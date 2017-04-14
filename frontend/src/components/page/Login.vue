<template>
    <div class="login-wrap">
        <div class="ms-title">数据挖掘平台</div>
        <div class="ms-login">
            <el-form :model="form" :rules="rules" ref="form" label-width="0px" class="demo-ruleForm">
                <el-form-item prop="username">
                    <el-input v-model="form.username" placeholder="username"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input type="password" placeholder="password" v-model="form.password" @keyup.enter.native="submitForm('form')"></el-input>
                </el-form-item>
                <div class="login-btn">
                    <el-button type="primary" @click="submitForm('form')">登录</el-button>
                </div>
                <p style="font-size:12px;line-height:30px;color:#999;">root:root1234</p>
            </el-form>
        </div>
    </div>
</template>

<script>
    export default {
        data: function() {
            return {
                form: {
                    username: '',
                    password: ''
                },
                rules: {
                    username: [{
                        required: true,
                        message: '请输入用户名',
                        trigger: 'blur'
                    }],
                    password: [{
                        required: true,
                        message: '请输入密码',
                        trigger: 'blur'
                    }]
                }
            }
        },
        methods: {
            submitForm(formName) {
                const self = this;
                self.$refs[formName].validate((valid) => {
                    if (valid) {
                        // 这里先发送请求
                        this.$http.post(API_ROOT + 'status/login',
                                this.$data.form, {
                                    headers: {
                                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                                    }
                                })
                            .then((response) => { // 正确回调
                                this.$notify({
                                    title: response.data['code'],
                                    message: response.data['message'],
                                    duration: 0,
                                });
                                // token 获取成功
                                var data = response.data['data']
                                localStorage.setItem('token', data['token']);
                                localStorage.setItem('username', data['username']);
                                // 这里还应该更新对应的权限
                                self.$router.push('/home');
                            })
                            .catch((error) => { // 即返回 404
                                this.$notify({
                                    title: error.response.data['code'],
                                    message: error.response.data['message'],
                                    duration: 2000,
                                });
                                this.resetForm(formName);
                            });
    
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            }
        }
    }
</script>

<style scoped>
    .login-wrap {
        position: relative;
        width: 100%;
        height: 100%;
    }
    
    .ms-title {
        position: absolute;
        top: 50%;
        width: 100%;
        margin-top: -230px;
        text-align: center;
        font-size: 30px;
        color: #fff;
    }
    
    .ms-login {
        position: absolute;
        left: 50%;
        top: 50%;
        width: 300px;
        height: 160px;
        margin: -150px 0 0 -190px;
        padding: 40px;
        border-radius: 5px;
        background: #fff;
    }
    
    .login-btn {
        text-align: center;
    }
    
    .login-btn button {
        width: 100%;
        height: 36px;
    }
</style>