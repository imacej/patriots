<template>
    <div class="table">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-menu"></i> 数据集中心</el-breadcrumb-item>
                <el-breadcrumb-item>训练集列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <p>类型：1-训练集，2-测试集</p>
        <p>格式：1-EXCEL，2-CSV，3-TXT，4-BINARY</p>
        <br/>
        <el-table :data="datasets" border style="width: 100%">
            <el-table-column prop="dname" label="名称" sortable>
            </el-table-column>
            <el-table-column prop="dpath" label="路径" sortable>
            </el-table-column>
            <el-table-column prop="dtype" label="类型" sortable>
            </el-table-column>
            <el-table-column prop="dformat" label="格式" sortable>
            </el-table-column>
            <el-table-column prop="dnote" label="备注">
            </el-table-column>
            <el-table-column label="操作" width="180">
                <template scope="scope">
                    <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
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
                datasets: [],
                count: 0,
            }
        },
        mounted() {
            this.getDatasets();
        },
        methods: {
            formatter(row, column) {
                return row.address;
            },
            filterTag(value, row) {
                return row.tag === value;
            },
            handleEdit(index, row) {
                this.$message('编辑第' + (index + 1) + '行');
            },
            handleDelete(index, row) {
                this.$confirm('此操作将永久删除该数据集, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$http.post('http://localhost:5000/datasets/' + this.datasets[index].id + '/delete', {}, {
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                            }
                        })
                        .then(response => {
                            this.datasets = response.body
                            this.count = this.datasets.length
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
            getDatasets() {
                this.$http
                    .get('http://localhost:5000/datasets')
                    .then(response => {
                        this.datasets = response.body
                        this.count = this.datasets.length
                    }, response => {
                        this.datasets = []
                        this.$message({
                            type: 'info',
                            message: '请求发送失败'
                        });
                    })
            }
        }
    }
</script>