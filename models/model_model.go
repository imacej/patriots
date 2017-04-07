package models

import (
	"time"

	"github.com/astaxie/beego/orm"
)

// Model 模型的数据结构
type Model struct {
	ID        int       `json:"id" orm:"column(id);pk;auto"`              // 自增 ID
	Name      string    `json:"name"`                                     // 模型名称
	Path      string    `json:"path"`                                     // 模型文件所在路径
	Note      string    `json:"note" orm:"null"`                          // 模型备注
	InTime    time.Time `json:"intime" orm:"auto_now_add;type(datetime)"` // 创建时间
	TrainTime time.Time `json:"traintime" orm:"type(datetime)"`           // 训练开始时间

	Algorithm  *Algorithm  `json:"algorithm" orm:"rel(one)"`      // 所使用的算法
	Trainset   *Trainset   `json:"trainset" orm:"rel(one)"`       // 所使用的训练集
	Validation *Validation `json:"validation" orm:"reverse(one)"` // 所对应的验证测试
}

func init() {
	orm.RegisterModel(new(Model))
}

// CreateModel 新建一个模型
func CreateModel(model *Model) (int64, error) {
	o := orm.NewOrm()
	id, err := o.Insert(model)
	return id, err
}

// GetModelByID 检索模型
func GetModelByID(id int) (*Model, error) {
	o := orm.NewOrm()
	var model Model
	err := o.QueryTable(model).Filter("id", id).One(&model)
	return &model, err
}

// DeleteModel 删除模型
func DeleteModel(model *Model) (int64, error) {
	o := orm.NewOrm()
	return o.Delete(model)
}

// GetModelList 获取模型列表
func GetModelList() []*Model {
	o := orm.NewOrm()
	var ModelList []*Model
	o.QueryTable(new(Model)).All(&ModelList)
	return ModelList
}
