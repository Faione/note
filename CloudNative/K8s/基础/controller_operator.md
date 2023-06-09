# Controller 


## Controller Manager

Controller Manager 用来管理不同的 Controller, 这些 Controller 会尽力保证目标对象的状态与用户声明的状态一致

## Controller

Controller 会定期通过 Api Server 与 etcd 进行同步，感知集群中对象状态的变化，并生成 Event 并下发给对应的 Controller, 而在对应 Controller 的内部逻辑中，会按照自己所管理的资源的特点进行调整以使得目标对象状态与用户声明的相符合

`client go` 与 `Controller runtime` 是实现 Controller 必不可少的部分

## Operator

Operator 与 Controller 功能类似，需要用户来实现其中 "调谐" 的过程，从而使得 CRD 能够达到用户所期望的状态
