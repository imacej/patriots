package models

import (
	"github.com/astaxie/beego/orm"
)

func init() {
	orm.RegisterModel(new(Model))
}

type Model struct {
	Id         int         // 自增 ID
	Name       string      // 模型名称
	Path       string      // 模型文件所在路径
	Algorithm  *Algorithm  `orm:"rel(one)"` // 所使用的算法
	Trainset   *Trainset   `orm:"rel(one)"` // 所使用的训练集
	Note       string      // 模型备注
	CreateTime string      // 创建时间
	TrainTime  string      // 训练开始时间
	Validation *Validation `orm:"reverse(one)"` // 所对应的验证测试
}
