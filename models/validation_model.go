package models

import (
	"time"

	"github.com/astaxie/beego/orm"
)

func init() {
	orm.RegisterModel(new(Validation))
}

// Validation 验证模型数据结构
type Validation struct {
	ID           int       `json:"id" orm:"column(id);pk;auto"` // 自增 ID
	Name         string    `json:"name"`                        // 测试集名称
	Path         string    `json:"path"`
	Note         string    `json:"note" orm:"null"`                          // 测试集备注
	InTime       time.Time `json:"intime" orm:"auto_now_add;type(datetime)"` // 创建时间
	ValidateTime time.Time `json:"validatetime" orm:"type(datetime)"`        // 验证开始时间

	Model   *Model   `orm:"rel(one)"` // 所使用的算法
	Testset *Testset `orm:"rel(one)"` // 所使用的测试集
}
