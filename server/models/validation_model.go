package models

import (
	"time"

	"github.com/astaxie/beego/orm"
)

// Validation 验证模型数据结构
type Validation struct {
	ID           int       `json:"id" orm:"column(id);pk;auto"` // 自增 ID
	Name         string    `json:"name"`                        // 测试集名称
	Path         string    `json:"path"`
	Note         string    `json:"note" orm:"null"`                          // 测试集备注
	InTime       time.Time `json:"intime" orm:"auto_now_add;type(datetime)"` // 创建时间
	ValidateTime time.Time `json:"validatetime" orm:"type(datetime)"`        // 验证开始时间

	Model   *Model   `json:"model" orm:"rel(one)"`   // 所使用的算法
	Testset *Testset `json:"testset" orm:"rel(one)"` // 所使用的测试集
}

func init() {
	orm.RegisterModel(new(Validation))
}

// CreateValidation 新建一个验证
func CreateValidation(validation *Validation) (int64, error) {
	o := orm.NewOrm()
	return o.Insert(validation)
}

// GetValidationByID 检索验证
func GetValidationByID(id int) (*Validation, error) {
	o := orm.NewOrm()
	var validation Validation
	err := o.QueryTable(validation).Filter("id", id).One(&validation)
	return &validation, err
}

// DeleteValidation 删除验证
func DeleteValidation(validation *Validation) (int64, error) {
	o := orm.NewOrm()
	return o.Delete(validation)
}

// GetValidationList 获取验证列表
func GetValidationList() []*Validation {
	o := orm.NewOrm()
	var ValidationList []*Validation
	o.QueryTable(new(Validation)).All(&ValidationList)
	return ValidationList
}
