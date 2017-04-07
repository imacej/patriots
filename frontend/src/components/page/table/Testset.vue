<template>
    <div class="table">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-menu"></i> 数据集中心</el-breadcrumb-item>
                <el-breadcrumb-item>测试集列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <br/>
        <el-table :data="list" border style="width: 100%">
            <el-table-column prop="name" label="名称" sortable>
            </el-table-column>
            <el-table-column prop="path" label="路径" sortable>
            </el-table-column>
            <el-table-column prop="type" label="类型" sortable>
            </el-table-column>
            <el-table-column prop="format" label="格式" sortable>
            </el-table-column>
            <el-table-column prop="note" label="备注">
            </el-table-column>

            <el-table-column label="操作" width="170">
                <template scope="scope">
                            <el-button-group>
                                <el-tooltip class="item" effect="dark" content="查看" placement="top">
                                    <el-button size="small" type="success" icon="information" @click="handleDetail(scope.$index, scope.row)"></el-button>
                                </el-tooltip>
                                <el-tooltip class="item" effect="dark" content="编辑" placement="top">
                                    <el-button size="small" type="primary" icon="edit" @click="handleEdit(scope.$index, scope.row)"></el-button>
                                </el-tooltip>
                                <el-tooltip class="item" effect="dark" content="删除" placement="top">
                                    <el-button size="small" type="danger" icon="delete" @click="handleDelete(scope.$index, scope.row)"></el-button>
                                </el-tooltip>
                            </el-button-group>
</template>
            </el-table-column>
        </el-table>
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
                list: [],
                count: 0
            }
        },
        mounted() {
            this.getTestsetList();
        },
        methods: {
            handleDetail(index, row) {
                this.$message('查看详情第' + (index + 1) + '行');
            },
            handleEdit(index, row) {
                this.$message('编辑第' + (index + 1) + '行');
            },
            handleDelete(index, row) {
                this.$confirm('此操作将永久删除该测试集, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$http.post('http://localhost:12333/v1/testsets/' + this.list[index].id + '/delete', {}, {
                            headers: {
                                'Authorization': 'Bearer ' + localStorage.getItem('token'),
                                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                            }
                        })
                        .then((response) => {
                            this.list = response.data
                            this.count = this.list.length
                        })
                        .catch((error) => {
                            this.$message({
                                type: 'error',
                                message: '删除失败'
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
            getTestsetList() {
                this.$http.get('http://localhost:12333/v1/testsets', {
                        headers: {
                            'Authorization': 'Bearer ' + localStorage.getItem('token'),
                        }
                    })
                    .then((response) => {
                        this.list = response.data
                        this.count = this.list.length
                    })
                    .catch((error) => {
                        this.list = []
                        this.count = 0
                    })
            }
        }
    }
</script>