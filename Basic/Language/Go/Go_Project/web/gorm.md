# Gorm

- [gorm](https://github.com/go-gorm/gorm)

```go
import (
	"fmt"
	"testing"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var (
	USER     = `fhl`
	PASS     = `123456`
	ADDRESS  = `127.0.0.1:3308`
	DATABASE = `gromtest`
)

type User struct {
	gorm.Model
	Name     string
	Password string
}

func connectMysql() *gorm.DB {
	dsn := fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=utf8mb4&parseTime=True&loc=Local", USER, PASS, ADDRESS, DATABASE)
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		panic("falied to connect mysql")
	}
	return db
}

func TestConnectMysql(t *testing.T) {
	_ = connectMysql()
	fmt.Println("mysql connected")
}

func TestCreateTable(t *testing.T) {
	db := connectMysql()

	if err := db.AutoMigrate(&User{}); err != nil {
		t.Errorf("migrate data failed: %s", err)
	}
}

func TestCreateUser(t *testing.T) {
	db := connectMysql()

	db.Create(&User{Name: "fhl", Password: "123"})
}

func TestSelectUser(t *testing.T) {
	db := connectMysql()

	var user User
	// mysql的查询默认不区分大小写，故 name 与 Name 都可以
	db.First(&user, "Name = ?", "fhl")
	fmt.Println(user)
}

func TestSelectUserByWhere(t *testing.T) {
	db := connectMysql()

	var user User
	// 字符串需要使用 ''
	db.Where("name = 'fhl'").Find(&user)
	fmt.Println(user)
}

func TestUpdateUser(t *testing.T) {
	db := connectMysql()

	var user User
	db.First(&user, "name = ?", "fhl")

	db.Model(&user).Update("password", "111")
	fmt.Println(user)
}

func TestSoftDeleteUser(t *testing.T) {
	db := connectMysql()

	var user User
	db.First(&user, "name = ?", "fhl")
	db.Delete(&user, user.ID)
}

func TestPermanentDeleteUser(t *testing.T) {
	db := connectMysql()

	var user User
	db.Unscoped().First(&user, "name = ?", "fhl")
	db.Unscoped().Delete(&user, user.ID)
}
```