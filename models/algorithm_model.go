package models

import (
	"time"

	"github.com/astaxie/beego/orm"
)

func init() {
	orm.RegisterModel(new(Algorithm))
}

// Algorithm 算法的数据结构
type Algorithm struct {
	ID     int       `json:"id" orm:"column(id);pk;auto"`              // 自增 ID
	Name   string    `json:"name"`                                     // 算法名称
	Path   string    `json:"path"`                                     // 算法文件所在路径
	Note   string    `json:"note" orm:"null"`                          // 算法备注
	InTime time.Time `json:"intime" orm:"auto_now_add;type(datetime)"` // 创建时间
	Model  *Model    `orm:"reverse(one)"`                              // 算法对应的模型
}
