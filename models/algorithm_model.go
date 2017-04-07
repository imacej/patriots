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
	Model  *Model    `json:"model" orm:"reverse(one)"`                 // 算法对应的模型
}

// CreateAlgorithm 新建一个训练集
func CreateAlgorithm(algorithm *Algorithm) (int64, error) {
	o := orm.NewOrm()
	id, err := o.Insert(algorithm)
	return id, err
}

// GetAlgorithmByID 检索训练集
func GetAlgorithmByID(id int) (*Algorithm, error) {
	o := orm.NewOrm()
	var algorithm Algorithm
	err := o.QueryTable(algorithm).Filter("id", id).One(&algorithm)
	return &algorithm, err
}

// DeleteAlgorithm 删除训练集
func DeleteAlgorithm(algorithm *Algorithm) (int64, error) {
	o := orm.NewOrm()
	return o.Delete(algorithm)
}

// GetAlgorithmList 获取训练集
func GetAlgorithmList() []*Algorithm {
	o := orm.NewOrm()
	var AlgorithmList []*Algorithm
	o.QueryTable(new(Algorithm)).All(&AlgorithmList)
	return AlgorithmList
}
