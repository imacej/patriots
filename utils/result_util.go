package utils

// Result 返回结果的数据结构
type Result struct {
	Code    int         `json:"code"`
	Message string      `json:"message"`
	Data    interface{} `json:"data"`
}

// MagicRoot 管理员的权限组
func MagicRoot() int {
	return -911
}
