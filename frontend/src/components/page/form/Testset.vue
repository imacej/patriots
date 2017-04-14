<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-date"></i> 数据集中心</el-breadcrumb-item>
                <el-breadcrumb-item>新建测试集</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="form-box">
            <p>测试集命名规则，test.txt</p>
            <br/>
            <el-form ref="form" :model="form" label-width="80px" :rules="rules">
                <el-form-item label="名称" prop="name">
                    <el-input v-model="form.name" placeholder="数据集名称"></el-input>
                </el-form-item>

                <el-form-item label="类别" prop="type">
                    <el-select v-model="form.type" placeholder="请选择">
                        <el-option label="二分类" value="binary"></el-option>
                        <el-option label="多分类" value="multi"></el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="格式" prop="format">
                    <el-select v-model="form.format" placeholder="请选择">
                        <el-option label="EXCEL" value="excel"></el-option>
                        <el-option label="CSV" value="csv"></el-option>
                        <el-option label="TXT" value="txt"></el-option>
                        <el-option label="BIN" value="bin"></el-option>
                    </el-select>
                </el-form-item>
    
                <el-form-item label="备注" prop="note">
                    <el-input type="textarea" v-model="form.note" placeholder="关于数据集的信息"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm('form')">新建数据集</el-button>
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
                    format: '',
                    type: '',
                    note: ''
                },
                rules: {
                    name: [{
                            required: true,
                            message: '请输入测试集名称',
                            trigger: 'blur'
                        },
                        {
                            min: 3,
                            max: 40,
                            message: '长度在 3 到 40 个字符',
                            trigger: 'blur'
                        }
                    ],
                    type: [{
                        required: true,
                        message: '请选择分类类型',
                        trigger: 'change'
                    }],
                    format: [{
                        required: true,
                        message: '请选择数据格式',
                        trigger: 'change'
                    }]
                }
            }
        },
        methods: {
            submitForm(formName) {
                var token = 'Bearer ' + localStorage.getItem('token')
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.$http.post(API_ROOT + 'testsets',
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