<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-date"></i> 数据集中心</el-breadcrumb-item>
                <el-breadcrumb-item>新建测试集</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="form-box">
            <p>训练集命名规则，正 pos.xls, 负 neg.xls（暂时只支持二类）</p>
            <p>测试集命名规则，test.txt</p>
            <br/>
            <el-form ref="form" :model="form" label-width="80px" :rules="rules">
                <el-form-item label="名称" prop="name">
                    <el-input v-model="form.name" placeholder="数据集名称"></el-input>
                </el-form-item>
    
                <el-form-item label="类型" prop="type">
                    <el-select v-model="form.type" placeholder="请选择">
                        <el-option label="训练集" value=1></el-option>
                        <el-option label="测试集" value=2></el-option>
                    </el-select>
                </el-form-item>
    
                <el-form-item label="格式" prop="format">
                    <el-select v-model="form.format" placeholder="请选择">
                        <el-option label="EXCEL" value=1></el-option>
                        <el-option label="CSV" value=2></el-option>
                        <el-option label="TXT" value=3></el-option>
                        <el-option label="BINARY" value=4></el-option>
                    </el-select>
                </el-form-item>
    
                <el-form-item label="备注">
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
                    type: '',
                    format: '',
                    note: ''
                },
                rules: {
                    name: [{
                            required: true,
                            message: '请输入数据集名称',
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
                        message: '请选择数据集类型',
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
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.$http.post('http://localhost:5000/datasets',
                            JSON.stringify(this.$data.form), {
                                headers: {
                                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                                }
                            }).then(
                            function(response) { // 正确回调
                                this.$notify({
                                    title: response.data['title'],
                                    message: response.data['info'],
                                    duration: 0,
                                });
                            },
                            function(response) { // 错误回调
                                this.$message.success('提交成功！');
                            });
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            },
        }
    }
</script>