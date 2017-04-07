package models

import (
	"time"

	"github.com/astaxie/beego"
	"github.com/astaxie/beego/orm"
)

// SystemAdmin 系统管理员
type User struct {
	ID       int       `json:"id" orm:"column(id);pk;auto"`
	Username string    `json:"username" orm:"unique;index"` // 用户名
	Password string    `json:"password"`
	Email    string    `json:"email" orm:"index"`
	InTime   time.Time `json:"intime" orm:"auto_now_add;type(datetime)"` // 启动时间
	Note     string    `json:"note" orm:"null"`                          // 备注
}

func init() {
	orm.RegisterModel(new(User))
}

// CreateUser 是用于新建一个系统管理员
func CreateUser(user *User) (int64, error) {
	beego.Trace("创建用户 用户名为", user.Username)
	o := orm.NewOrm()
	id, err := o.Insert(user)
	return id, err
}

// GetUserByID 检索系统管理员
func GetUserByID(id int) (*User, error) {
	o := orm.NewOrm()
	var user User
	err := o.QueryTable(user).Filter("id", id).One(&user)
	return &user, err
}

// GetUserByUsername 检索系统管理员
func GetUserByUsername(username string) (*User, error) {
	o := orm.NewOrm()
	var user User
	err := o.QueryTable(user).Filter("username", username).One(&user)
	return &user, err
}

// DeleteUser 删除系统管理员
func DeleteUser(user *User) (int64, error) {
	beego.Trace("删除用户 用户名为", user.Username)
	o := orm.NewOrm()
	return o.Delete(user)
}

// GetUserList 获取系统管理员列表
func GetUserList() []*User {
	beego.Trace("获取用户列表")
	o := orm.NewOrm()
	var UserList []*User
	o.QueryTable(new(User)).All(&UserList)
	return UserList
}
