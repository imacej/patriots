package utils

import (
	"time"

	"github.com/astaxie/beego"
	jwt "github.com/dgrijalva/jwt-go"
)

// 加密的密钥
var (
	key = []byte("patroits-jwt-secret")
)

// IdentityClaims Token 中包含的信息
type IdentityClaims struct {
	UserID int    `json:"uid"`
	Type   string `json:"type"`
	jwt.StandardClaims
}

// GenerateToken 根据登录信息生成 Token
func GenerateToken(uid int, t string) (string, error) {
	claims := IdentityClaims{
		uid,
		t,
		jwt.StandardClaims{
			NotBefore: int64(time.Now().Unix()),
			IssuedAt:  int64(time.Now().Unix()),
			ExpiresAt: int64(time.Now().Unix() + 36000),
			Issuer:    "patriots",
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(key)
}

// ParseToken 验证是否是有效 Token
func ParseToken(tokenString string) (*IdentityClaims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &IdentityClaims{}, func(token *jwt.Token) (interface{}, error) {
		return key, nil
	})

	if claims, ok := token.Claims.(*IdentityClaims); ok && token.Valid {
		// 验证成功，返回信息
		return claims, err
	}

	// 验证失败
	beego.Error("Token 验证失败", err)
	return nil, err
}
