<template>
    <div class="table">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-menu"></i> 算法中心</el-breadcrumb-item>
                <el-breadcrumb-item>算法列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <el-table :data="algorithms" border style="width: 100%">
            <el-table-column prop="aname" label="名称" >
            </el-table-column>

            <el-table-column prop="apath" label="路径">
            </el-table-column>
            <el-table-column prop="anote" label="说明">
            </el-table-column>
            
            <el-table-column label="操作" width="180">
                <template scope="scope">
                    <el-button size="small"
                            @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button size="small" type="danger"
                            @click="handleDelete(scope.$index, scope.row)">删除</el-button>
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
                algorithms: [],
                count: 0
            }
        },
        mounted() {
            this.getAlgorithms();
        },
        methods: {
            formatter(row, column) {
                return row.address;
            },
            filterTag(value, row) {
                return row.tag === value;
            },
            handleEdit(index, row) {
                this.$message('编辑第'+(index+1)+'行');
            },
            handleDelete(index, row) {
                this.$confirm('此操作将永久删除该算法（不会删除文件）, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$http.post('http://localhost:5000/algorithms/' + this.algorithms[index].id + '/delete', {}, {
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                            }
                        })
                        .then(response => {
                            this.algorithms = response.body
                            this.count = this.algorithms.length
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
            getAlgorithms() {
                this.$http
                    .get('http://localhost:5000/algorithms')
                    .then(response => {
                        this.algorithms = response.body
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