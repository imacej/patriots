package models

import (
	"github.com/astaxie/beego/orm"
)

func init() {
	orm.RegisterModel(new(Algorithm))
}

type Algorithm struct {
	Id         int    // 自增 ID
	Name       string // 算法名称
	Path       string // 算法文件所在路径
	Note       string // 算法备注
	CreateTime string // 创建时间
	Model      *Model `orm:"reverse(one)"` // 算法对应的模型
}
