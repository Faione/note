## 接口设计

- [接口设计](#接口设计)
  - [菜品CRUD](#菜品crud)
  - [菜单CRUD](#菜单crud)
  - [评价CRUD](#评价crud)
  - [订单CRUD](#订单crud)

### 菜品CRUD

**增加菜品**

[post] /v1/dish
 
**删除菜品**

[delete] /v1/dish/{dish_id}


**修改菜品**

[update] /v1/dish/{dish_id}


**查询菜品**

[get] /v1/dish/{dish_id}


[get] /v1/dishs

### 菜单CRUD

**增加菜单**

[post] /v1/menu


**删除菜单**

[delete] /v1/menu/{menu_id}


**修改菜单**

[update] /v1/menu/{menu_id}


**查询菜单**

[get] /v1/menu/{menu_id}

[get] /v1/menus

### 评价CRUD

**增加评价**

[post] /v1/assessment


**删除评价**

[delete] /v1/assessment/{assessment_id}


**修改评价**

[update] /v1/assessment/{assessment_id}


**查询评价**

[get] /v1/assessment/{assessment_id}

[get] /v1/assessments


### 订单CRUD

**增加订单**

[post] /v1/order


**删除订单**

[delete] /v1/order/{order_id}


**查询订单**

[get] /v1/order/{order_id}


[get] /v1/orders