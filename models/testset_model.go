package models

import (
	"time"

	"github.com/astaxie/beego/orm"
)

// Testset 测试集数据结构
type Testset struct {
	ID         int         `json:"id" orm:"column(id);pk;auto"`              // 自增 ID
	Name       string      `json:"name"`                                     // 测试集名称
	Path       string      `json:"path"`                                     // 测试集文件所在路径
	Type       string      `json:"type"`                                     // 测试集分类（二类、多类）
	Format     string      `json:"format"`                                   // 测试集格式（xls, csv, txt, binary..)
	Note       string      `json:"note" orm:"null"`                          // 测试集备注
	InTime     time.Time   `json:"intime" orm:"auto_now_add;type(datetime)"` // 创建时间
	Validation *Validation `json:"validation" orm:"reverse(one)"`            // 所对应的模型
}

func init() {
	orm.RegisterModel(new(Testset))
}

// CreateTestset 新建一个测试集
func CreateTestset(testset *Testset) (int64, error) {
	o := orm.NewOrm()
	id, err := o.Insert(testset)
	return id, err
}

// GetTestsetByID 检索测试集
func GetTestsetByID(id int) (*Testset, error) {
	o := orm.NewOrm()
	var testset Testset
	err := o.QueryTable(testset).Filter("id", id).One(&testset)
	return &testset, err
}

// DeleteTestset 删除测试集
func DeleteTestset(testset *Testset) (int64, error) {
	o := orm.NewOrm()
	return o.Delete(testset)
}

// GetTestsetList 获取测试集列表
func GetTestsetList() []*Testset {
	o := orm.NewOrm()
	var TestsetList []*Testset
	o.QueryTable(new(Testset)).All(&TestsetList)
	return TestsetList
}
