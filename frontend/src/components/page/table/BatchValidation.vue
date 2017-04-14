<template>
    <div class="table">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-menu"></i> 测试中心</el-breadcrumb-item>
                <el-breadcrumb-item>批量测试列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
    
        <el-table :data="models" border style="width: 100%">
            <el-table-column prop="tname" label="名称" width="300">
            </el-table-column>
            <el-table-column prop="tmodelid" label="算法" sortable>
            </el-table-column>
            <el-table-column prop="ttestsetid" label="测试集" sortable>
            </el-table-column>
            <el-table-column prop="tnote" label="说明" width="500">
            </el-table-column>
            <el-table-column label="操作" width="200">
                <template scope="scope">
                    <el-button-group>
                        <el-tooltip class="item" effect="dark" content="查看测试统计信息" placement="top">
                            <el-button size="small" type="success" icon="information" @click="handleStatus(scope.$index, scope.row)"></el-button>
                        </el-tooltip>
                        <el-tooltip class="item" effect="dark" content="查看测试日志信息" placement="top">
                            <el-button size="small" type="warning" icon="view" @click="handleLog(scope.$index, scope.row)"></el-button>
                        </el-tooltip>
                        <el-tooltip class="item" effect="dark" content="开始测试" placement="top">
                            <el-button size="small" type="primary" icon="time" @click="handleTrain(scope.$index, scope.row)"></el-button>
                        </el-tooltip>
                        <el-tooltip class="item" effect="dark" content="删除测试" placement="top">
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
            this.getTests();
        },
        methods: {
            formatter(row, column) {
                return row.address;
            },
            filterTag(value, row) {
                return row.tag === value;
            },
            handleStatus(index, row) {
                this.$http.get(API_ROOT + 'tests/' + this.models[index].id + '/result')
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
                this.$http.get(API_ROOT + 'tests/' + this.models[index].id + '/log')
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
                this.$confirm('确定要开始/重新测试吗?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$http.post(API_ROOT + 'tests/' + this.models[index].id + '/start', {}, {
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
                        message: '已取消测试'
                    });
                });
    
    
            },
            handleDelete(index, row) {
                this.$confirm('此操作将永久删除该数据集, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$http.post(API_ROOT + 'tests/' + this.models[index].id + '/delete', {}, {
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
            getTests() {
                this.$http
                    .get('http://127.0.0.1:5000/tests')
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