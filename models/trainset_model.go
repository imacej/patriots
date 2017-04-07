package models

import (
	"time"

	"github.com/astaxie/beego/orm"
)

// Trainset 训练集数据结构
type Trainset struct {
	ID     int       `json:"id" orm:"column(id);pk;auto"`              // 自增 ID
	Name   string    `json:"name"`                                     // 训练集名称
	Path   string    `json:"path"`                                     // 训练集文件所在路径
	Type   string    `json:"type"`                                     // 训练集分类（二类、多类）
	Format string    `json:"format"`                                   // 训练集格式（xls, csv, txt, binary..)
	Note   string    `json:"note" orm:"null"`                          // 训练集备注
	InTime time.Time `json:"intime" orm:"auto_now_add;type(datetime)"` // 创建时间
	Model  *Model    `json:"model" orm:"reverse(one)"`                 // 所对应的模型                             // 所对应的模型
}

func init() {
	orm.RegisterModel(new(Trainset))
}

// CreateTrainset 新建一个训练集
func CreateTrainset(trainset *Trainset) (int64, error) {
	o := orm.NewOrm()
	id, err := o.Insert(trainset)
	return id, err
}

// GetTrainsetByID 检索训练集
func GetTrainsetByID(id int) (*Trainset, error) {
	o := orm.NewOrm()
	var trainset Trainset
	err := o.QueryTable(trainset).Filter("id", id).One(&trainset)
	return &trainset, err
}

// DeleteTrainset 删除训练集
func DeleteTrainset(trainset *Trainset) (int64, error) {
	o := orm.NewOrm()
	return o.Delete(trainset)
}

// GetTrainsetList 获取训练集
func GetTrainsetList() []*Trainset {
	o := orm.NewOrm()
	var TrainsetList []*Trainset
	o.QueryTable(new(Trainset)).All(&TrainsetList)
	return TrainsetList
}
