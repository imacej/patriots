<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-date"></i> 测试中心</el-breadcrumb-item>
                <el-breadcrumb-item>单个测试</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="form-box">
            <p>选择需要测试的模型，输入问句进行测试，结果为 [positive] 或 [negative]</p>
            <br/>
            <el-form ref="form" :model="form" label-width="80px" :rules="rules">
                <el-form-item label="模型" prop="modelid">
                    <el-select v-model="form.modelid" filterable placeholder="请选择">
                        <el-option v-for="mo in models" :label="mo.label" :value="mo.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="问句" prop="sentence">
                    <el-input type="textarea" v-model="form.sentence"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm('form')">提交测试</el-button>
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
                    sentence: '',
                    modelid: ''
                },
                models: [],
                rules: {
                    modelid: [{
                        type: 'number',
                        required: true,
                        message: '请选择模型',
                        trigger: 'change'
                    }],
                    sentence: [{
                        required: true,
                        message: '请输入问句',
                        trigger: 'blur'
                    }]
                }
            }
        },
        mounted() {
            this.getModels();
        },
        methods: {
            getModels() {
                this.$http
                    .get('http://127.0.0.1:5000/models')
                    .then(response => {
                        this.models = response.body.map(mo => {
                            return {
                                label: mo.mname,
                                value: mo.id
                            }
                        })
                    }, response => {
                        this.models = []
                    })
            },
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.$http.post('http://localhost:5000/models/' + this.form.modelid + '/test',
                            JSON.stringify(this.$data.form), {
                                headers: {
                                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                                }
                            }).then(
                            function(response) { // 正确回调
                                this.$notify({
                                    title: '【结果】' + response.data[0],
                                    message: '【内容】' + response.data[1],
                                    duration: 0,
                                });
                            },
                            function(response) { // 错误回调
                                this.$message.success('提交失败！');
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