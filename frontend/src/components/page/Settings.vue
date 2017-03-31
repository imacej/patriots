<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-date"></i> 图书中心</el-breadcrumb-item>
                <el-breadcrumb-item>录入图书</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="form-box">
            <el-form ref="form" :model="form" label-width="80px">
                <el-form-item label="ISBN 13">
                    <el-input v-model="form.isbn13" placeholder="ISBN13"></el-input>
                </el-form-item>
                <el-form-item label="ISBN 9">
                    <el-input v-model="form.isbn9" placeholder="ISBN9"></el-input>
                </el-form-item>
                <el-form-item label="中文书名">
                    <el-input v-model="form.titleCN" placeholder="小王子"></el-input>
                </el-form-item>
                <el-form-item label="外文书名">
                    <el-input v-model="form.titleForeign" placeholder="Little Prince"></el-input>
                </el-form-item>
                <el-form-item label="作者">
                    <el-input v-model="form.author" placeholder="圣埃克苏佩里"></el-input>
                </el-form-item>
                <el-form-item label="译者">
                    <el-input v-model="form.translator" placeholder="李继宏"></el-input>
                </el-form-item>
                <el-form-item label="出版社">
                    <el-input v-model="form.publisher" placeholder="天津人民出版社"></el-input>
                </el-form-item>
    
                <el-form-item label="出版时间">
                    <el-date-picker type="date" placeholder="选择日期" v-model="form.publishDate" style="width: 100%;"></el-date-picker>
                </el-form-item>
    
                <el-form-item label="价格">
                    <el-input v-model.number="form.price" value="number" placeholder="0.00">
                        <template slot="prepend">￥
</template>
                    </el-input>
                </el-form-item>


                <el-form-item label="图书馆">
                    <el-select v-model="form.library" filterable placeholder="请选择">
                        <el-option
                        v-for="lib in libraries"
                        :label="lib.label"
                        :value="lib.value">
                        </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="备注">
                    <el-input type="textarea" v-model="form.note"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="onSubmit">提交</el-button>
                    <el-button>取消</el-button>
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
                    //ISBN code
                    isbn13: '', // ISBN 13
                    isbn9: '', // ISBN 9
    
                    //Book Info
                    titleCN: '', // 中文书名
                    titleForeign: '', // 英文书名
                    author: '', // 作者
                    translator: '', // 译者
                    publisher: '', // 出版社
                    publishDate: '', // 出版时间
                    price: 0, // 定价
                    note: '', // 备注
                    library: '' // 图书馆
                },
                libraries: [{
                    label: "第一图书馆",
                    value: 1
                }]
            }
        },
        mounted() {
            this.retrieveLibraries();
        },
        methods: {
            onSubmit() {
                this.$message.success('提交成功！');
                console.log(this.$data.form)
                event.preventDefault()
                // $.ajax({
                //     type: "POST",
                //     url: 'http://localhost:8080/books',
                //     processData: false,
                //     context: this,
                //     contentType: 'application/json',
                //     data: JSON.stringify(this.$data)
                // });
            },
            retrieveLibraries() {
                this.$http
                    .get('http://localhost:12333/v1/api/libraries', {
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                        }
                    })
                    .then(response => {
                        this.libraries = response.body.map(lib => {
                            return {
                                label: lib.Name,
                                value: lib.Id
                            }
                        })
                    }, response => {
                        this.libraries = []
                    })
            }
        }
    }
</script>