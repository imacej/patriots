<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-date"></i> 验证中心</el-breadcrumb-item>
                <el-breadcrumb-item>提交批量验证</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="form-box">
            <p>选择需要测试的模型，选择测试集合进行批量测试，结果可在批量测试列表中查看</p>
            <br/>
            <el-form ref="form" :model="form" label-width="80px" :rules="rules">
                <el-form-item label="名称" prop="name">
                    <el-input v-model="form.name" placeholder="批量测试名称"></el-input>
                </el-form-item>
                <el-form-item label="模型" prop="modelid">
                    <el-select v-model="form.modelid" filterable placeholder="请选择">
                        <el-option v-for="mo in models" :label="mo.label" :value="mo.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="测试集" prop="testsetid">
                    <el-select v-model="form.testsetid" filterable placeholder="请选择">
                        <el-option v-for="ds in datasets" :label="ds.label" :value="ds.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input type="textarea" v-model="form.note"></el-input>
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
                    modelid: '',
                    testsetid: '',
                    name: '',
                    note: '',
                },
                models: [],
                datasets: [],
                rules: {
                    name: [{
                            required: true,
                            message: '请输入模型名称',
                            trigger: 'blur'
                        },
                        {
                            min: 3,
                            max: 40,
                            message: '长度在 3 到 40 个字符',
                            trigger: 'blur'
                        }
                    ],
                    modelid: [{
                        type: 'number',
                        required: true,
                        message: '请选择模型',
                        trigger: 'change'
                    }],
                    testsetid: [{
                        type: 'number',
                        required: true,
                        message: '请选择测试集',
                        trigger: 'change'
                    }]
                }
            }
        },
        mounted() {
            this.getModels();
            this.getDatasets();
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
            getDatasets() {
                this.$http
                    .get(API_ROOT + 'datasets?type=test')
                    .then(response => {
                        this.datasets = response.body.map(ds => {
                            return {
                                label: ds.dname,
                                value: ds.id
                            }
                        })
                    }, response => {
                        this.datasets = []
                    })
            },
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.$http.post(API_ROOT + 'tests',
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