<template>
    <div class="table">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-menu"></i> 模型中心</el-breadcrumb-item>
                <el-breadcrumb-item>模型列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
    
        <el-table :data="models" border style="width: 100%">
            <el-table-column prop="mname" label="名称">
            </el-table-column>
            <el-table-column prop="malgoid" label="算法" sortable>
            </el-table-column>
            <el-table-column prop="mtrainsetid" label="训练集" sortable>
            </el-table-column>
            <el-table-column prop="mnote" label="说明">
            </el-table-column>
            <el-table-column label="操作" width="200">
                <template scope="scope">
                                <el-button-group>
                                    <el-tooltip class="item" effect="dark" content="查看训练统计信息" placement="top">
                                        <el-button size="small" type="success" icon="information" @click="handleStatus(scope.$index, scope.row)"></el-button>
                                    </el-tooltip>
                                    <el-tooltip class="item" effect="dark" content="查看训练日志信息" placement="top">
                                        <el-button size="small" type="warning" icon="view" @click="handleLog(scope.$index, scope.row)"></el-button>
                                    </el-tooltip>
                                    <el-tooltip class="item" effect="dark" content="开始训练（需要较长时间）" placement="top">
                                        <el-button size="small" type="primary" icon="time" @click="handleTrain(scope.$index, scope.row)"></el-button>
                                    </el-tooltip>
                                    <el-tooltip class="item" effect="dark" content="删除模型" placement="top">
                                        <el-button size="small" type="danger" icon="delete" @click="handleDelete(scope.$index, scope.row)"></el-button>
                                    </el-tooltip>
                                </el-button-group>
</template>
            </el-table-column>
        </el-table>
        
        <el-dialog title="日志" v-model="logVisible" size="small">
            <span v-for="line in logtext">{{ line }}<br/></span>
        </el-dialog>

        <el-dialog title="结果" v-model="resultVisible" size="small">
            <span v-for="line in resulttext">{{ line }}<br/></span>
        </el-dialog>

        <div class="pagination">
            <el-pagination
                    layout="prev, pager, next"
                    :total="count">
            </el-pagination>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                count: 0,
                models: [],
                logtext: '',
                logVisible: false,
                resulttext: '',
                resultVisible: false
            }
        },
        mounted() {
            this.getModels();
        },
        methods: {
            formatter(row, column) {
                return row.address;
            },
            filterTag(value, row) {
                return row.tag === value;
            },
            handleStatus(index, row) {
                this.$http.get(API_ROOT + 'models/' + this.models[index].id + '/result')
                    .then(
                        function(response) { // 正确回调
                            this.resulttext = response.data['result']
                            this.resultVisible = true
                        },
                        function(response) { // 错误回调
                            this.$message.success('日志获取失败！');
                        });
            },
            handleLog(index, row) {
                this.$http.get(API_ROOT + 'models/' + this.models[index].id + '/log')
                    .then(
                        function(response) { // 正确回调
                            this.logtext = response.data['log']
                            this.logVisible = true
                        },
                        function(response) { // 错误回调
                            this.$message.success('日志获取失败！');
                        });
            },
            handleTrain(index, row) {
                this.$confirm('确定要开始/重新训练吗?要花费较长时间', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$http.post(API_ROOT + 'models/' + this.models[index].id + '/train', {}, {
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
                            this.$message.success('训练提交失败！');
                        });
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消训练'
                    });
                });
    
    
            },
            handleDelete(index, row) {
                this.$confirm('此操作将永久删除该数据集, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$http.post(API_ROOT + 'models/' + this.models[index].id + '/delete', {}, {
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                            }
                        })
                        .then(response => {
                            this.models = response.body
                            this.count = this.models.length
                        }, response => {
                            this.$message({
                                type: 'info',
                                message: '请求发送失败'
                            });
                        })
                    this.$message({
                        type: 'success',
                        message: '删除成功'
                    });
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
            },
            getModels() {
                this.$http
                    .get('http://127.0.0.1:5000/models')
                    .then(response => {
                        this.models = response.body
                        this.count = this.models.length
                    }, response => {
                        this.models = []
                        this.count = 0
                    })
            }
        }
    }
</script>