# Test

## How To Write Test

1. Set up any needed data or state.
2. Run the code you want to test.
3. Assert the results are what you expect.


## 构造test

- 在方法前增加`#[test]`属性

- [test](https://doc.rust-lang.org/book/ch11-01-writing-tests.html)

## Assert

- assert!(condition)
- assert_eq!(target, real)
- assert_ne!(target, real)

**自定义assert失败时信息**

- 增加额外参数

```rust
assert!(
    result.contains("Carol"),
    "Greeting did not contain name, value was `{}`",
    result
);
```

**对于panic的处理**

- 程序处理过程中，会出现panic，则可在test中使用`#[should_panic]`属性进行panic的捕获
- 精确的should_panic
  - `#[should_panic(expected = "Guess value must be less than or equal to 100")]`

**使用Result**

```rust
#[cfg(test)]
mod tests {
    #[test]
    fn it_works() -> Result<(), String> {
        if 2 + 2 == 4 {
            Ok(())
        } else {
            Err(String::from("two plus two does not equal four"))
        }
    }
}
```

## 控制Tests的执行

- 默认情况下，cargo test 以多线程的方式运行Test
  - 需要注意Test之间的依赖
  - 可以设置线程数为`1`, 从而让Test串行

```shell
$ cargo test -- --test-threads=1
```
