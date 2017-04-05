package models

import (
	"time"

	"github.com/astaxie/beego/orm"
)

func init() {
	orm.RegisterModel(new(Trainset))
}

// Trainset 训练集数据结构
type Trainset struct {
	ID     int       `json:"id" orm:"column(id);pk;auto"`              // 自增 ID
	Name   string    `json:"name"`                                     // 测试集名称
	Path   string    `json:"path"`                                     // 测试集文件所在路径
	Type   int       `json:"type"`                                     // 测试集分类（二类、多类）
	Format int       `json:"format"`                                   // 测试集格式（xls, csv, txt, binary..)
	Note   string    `json:"note" orm:"null"`                          // 测试集备注
	InTime time.Time `json:"intime" orm:"auto_now_add;type(datetime)"` // 创建时间
	Model  *Model    `orm:"reverse(one)"`                              // 所对应的模型                             // 所对应的模型
}
