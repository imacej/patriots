package utils

// 各类错误信息的字符串

// Error400 客户端传入的参数不对
func Error400() string {
	return "参数解析错误"
}

// Error401 令牌无效或过期
func Error401() string {
	return "令牌无效或过期，请重新登录"
}

// Error403 客户端权限错误
func Error403() string {
	return "没有执行该动作的权限"
}

// Error404 无对应内容
func Error404() string {
	return "没有对应的内容，请检查后重试"
}

// Error500 服务器处理错误
func Error500() string {
	return "服务器错误"
}
