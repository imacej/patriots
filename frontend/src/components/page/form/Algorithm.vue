<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-date"></i> 算法中心</el-breadcrumb-item>
                <el-breadcrumb-item>新建算法</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="form-box">
            <p>这里说明算法需要的通用格式，比如说 train, predict 之类的</p>
            <p>注：配合具体的文档</p>
            <br/>
            <el-form ref="form" :model="form" label-width="80px" :rules="rules">
                <el-form-item label="名称" prop="name">
                    <el-input v-model="form.name" placeholder="LSTM"></el-input>
                </el-form-item>
                <el-form-item label="路径" prop="path">
                    <el-input v-model="form.path" placeholder="lstm.py">
                        <template slot="prepend">code/
</template>
                    </el-input>
                </el-form-item>
                <el-form-item label="备注" prop="note">
                    <el-input type="textarea" v-model="form.note"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm('form')">新建算法</el-button>
                    <el-button @click="resetForm('form')">重置</el-button>
                </el-form-item>
            </el-form>
        </div>
    
    </div>
</template>

<script>
    export default {
        data: function() {
            return {
                form: {
                    name: '',
                    path: '',
                    note: ''
                },
                rules: {
                    name: [{
                            required: true,
                            message: '请输入算法名称',
                            trigger: 'blur'
                        },
                        {
                            min: 3,
                            max: 40,
                            message: '长度在 3 到 40 个字符',
                            trigger: 'blur'
                        }
                    ],
                    path: [{
                        required: true,
                        message: '请输入算法文件路径',
                        trigger: 'blur'
                    }]
                }
            }
        },
        methods: {
            submitForm(formName) {
                var token = 'Bearer ' + localStorage.getItem('token')
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.$http.post('http://localhost:12333/v1/algorithms',
                            this.$data.form, {
                                headers: {
                                    'Authorization': token,
                                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                                }
                            })
                            .then((response) => { // 正确回调
                                this.$notify({
                                    title: response.data['code'],
                                    message: response.data['message'],
                                    duration: 0,
                                });
                                // 重置表单
                                this.resetForm(formName)
                            })
                            .catch((error) => {
                                this.$notify({
                                    title: error.response.data['code'],
                                    message: error.response.data['message'],
                                    duration: 2000,
                                });
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