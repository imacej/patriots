<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-date"></i> 模型中心</el-breadcrumb-item>
                <el-breadcrumb-item>新建模型</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="form-box">
            <el-form ref="form" :model="form" label-width="80px" :rules="rules">
                <el-form-item label="名称" prop="name">
                    <el-input v-model="form.name" placeholder="模型名称"></el-input>
                </el-form-item>
                <el-form-item label="算法" prop="algoid">
                    <el-select v-model="form.algoid" filterable placeholder="请选择">
                        <el-option
                        v-for="ds in algorithms"
                        :label="ds.label"
                        :value="ds.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="训练集" prop="trainsetid">
                    <el-select v-model="form.trainsetid" filterable placeholder="请选择">
                        <el-option
                        v-for="ds in datasets"
                        :label="ds.label"
                        :value="ds.value">
                        </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="备注">
                    <el-input type="textarea" v-model="form.note"></el-input>
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
        data() {
            return {
                form: {
                    trainsetid: '',
                    algoid: '',
                    name: '',
                    note: ''
                },
                datasets: [],
                algorithms: [],
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
                    algoid: [{
                        type: 'number',
                        required: true,
                        message: '请选择算法',
                        trigger: 'change'
                    }],
                    trainsetid: [{
                        type: 'number',
                        required: true,
                        message: '请选择训练集',
                        trigger: 'change'
                    }],
                }
            }
        },
        mounted() {
            this.getDatasets();
            this.getAlgorithms();
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.$http.post('http://localhost:5000/models',
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
            getDatasets() {
                this.$http
                    .get('http://localhost:5000/datasets?type=train')
                    .then(response => {
                        this.datasets = response.body.map(ds => {
                            return {
                                label: ds.dname,
                                value: ds.id
                            }
                        })
                        this.count = this.datasets.length
                    }, response => {
                        this.datasets = []
                    })
            },
            getAlgorithms() {
                this.$http
                    .get('http://localhost:5000/algorithms')
                    .then(response => {
                        this.algorithms = response.body.map(algo => {
                            return {
                                label: algo.aname,
                                value: algo.id
                            }
                        })
                        this.count = this.algorithms.length
                    }, response => {
                        this.algorithms = []
                        this.$message({
                            type: 'info',
                            message: '请求发送失败'
                        });
                    })
            }
        }
    }
</script>