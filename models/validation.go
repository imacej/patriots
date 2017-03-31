package models

import (
	"github.com/astaxie/beego/orm"
)

func init() {
	orm.RegisterModel(new(Validation))
}

type Validation struct {
	Id           int      // 自增 ID
	Name         string   // 验证名称
	Path         string   // 模型文件所在路径
	Model        *Model   `orm:"rel(one)"` // 所使用的算法
	Testset      *Testset `orm:"rel(one)"` // 所使用的测试集
	Note         string   // 模型备注
	CreateTime   string   // 创建时间
	ValidateTime string   // 验证开始时间
}
