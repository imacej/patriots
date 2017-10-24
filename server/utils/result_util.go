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

// ResultTokenCreated 返回创建的 Token
func ResultTokenCreated(username string, token string) Result {
	return Result{Code: 200, Message: "Token 创建成功", Data: map[string]string{"username": username, "token": token}}
}

//ResultTrainsetCreated 训练集创建成功
func ResultTrainsetCreated() Result {
	return Result{Code: 200, Message: "训练集创建成功"}
}

//ResultTestsetCreated 训练集创建成功
func ResultTestsetCreated() Result {
	return Result{Code: 200, Message: "测试集创建成功"}
}

//ResultAlgorithmCreated 算法创建成功
func ResultAlgorithmCreated() Result {
	return Result{Code: 200, Message: "算法创建成功，可以开始训练模型"}
}
