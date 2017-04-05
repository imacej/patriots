package models

import (
	"time"

	"github.com/astaxie/beego/orm"
)

func init() {
	orm.RegisterModel(new(Model))
}

// Model 模型的数据结构
type Model struct {
	ID        int       `json:"id" orm:"column(id);pk;auto"`              // 自增 ID
	Name      string    `json:"name"`                                     // 模型名称
	Path      string    `json:"path"`                                     // 模型文件所在路径
	Note      string    `json:"note" orm:"null"`                          // 模型备注
	InTime    time.Time `json:"intime" orm:"auto_now_add;type(datetime)"` // 创建时间
	TrainTime time.Time `json:"traintime" orm:"type(datetime)"`           // 训练开始时间

	Algorithm  *Algorithm  `orm:"rel(one)"`     // 所使用的算法
	Trainset   *Trainset   `orm:"rel(one)"`     // 所使用的训练集
	Validation *Validation `orm:"reverse(one)"` // 所对应的验证测试
}
