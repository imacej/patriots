package models

import (
	"github.com/astaxie/beego/orm"
)

func init() {
	orm.RegisterModel(new(Testset))
}

type Testset struct {
	Id         int         // 自增 ID
	Name       string      // 测试集名称
	Path       string      // 测试集文件所在路径
	Type       int         // 测试集分类（二类、多类）
	Format     int         // 测试集格式（xls, csv, txt, binary..)
	Note       string      // 测试集备注
	CreateTime string      // 创建时间
	Validation *Validation `orm:"reverse(one)"` // 所对应的模型
}
