package models

import (
	"github.com/astaxie/beego/orm"
)

func init() {
	orm.RegisterModel(new(Trainset))
}

type Trainset struct {
	Id         int    // 自增 ID
	Name       string // 训练集名称
	Path       string // 训练集文件所在路径
	Type       int    // 训练集分类（二类、多类）
	Format     int    // 训练集格式（xls, csv, txt, binary..)
	Note       string // 训练集备注
	CreateTime string // 创建时间
	Model      *Model `orm:"reverse(one)"` // 所对应的模型
}
