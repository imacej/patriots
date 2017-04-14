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
                        v-for="algo in algorithms"
                        :label="algo.label"
                        :value="algo.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="训练集" prop="trainsetid">
                    <el-select v-model="form.trainsetid" filterable placeholder="请选择">
                        <el-option
                        v-for="ts in trainsets"
                        :label="ts.label"
                        :value="ts.value">
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
                trainsets: [],
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
            this.getTrainsets();
            this.getAlgorithms();
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.$http.post(API_ROOT + 'models',
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
            },
            getTrainsets() {
                this.$http.get(API_ROOT + 'trainsets', {
                        headers: {
                            'Authorization': 'Bearer ' + localStorage.getItem('token'),
                        }
                    })
                    .then((response) => {
                        this.trainsets = response.data.map(ts => {
                            return {
                                label: ts.name,
                                value: ts.id
                            }
                        })
                    })
                    .catch((error) => {
                        this.trainsets = []
                    })
            },
            getAlgorithms() {
                this.$http.get(API_ROOT + 'algorithms', {
                        headers: {
                            'Authorization': 'Bearer ' + localStorage.getItem('token'),
                        }
                    })
                    .then((response) => {
                        this.algorithms = response.data.map(algo => {
                            return {
                                label: algo.name,
                                value: algo.id
                            }
                        })
                    })
                    .catch((error) => {
                        this.algorithms = []
                    })  
            }
        }
    }
</script>