<template>
    <div class="sidebar">
        <el-menu :default-active="onRoutes" class="el-menu-vertical-demo" theme="dark" unique-opened router>
            <el-menu-item index="readme">
                <i class="el-icon-view"></i>系统概况
            </el-menu-item>
            <el-submenu index="1">
                <template slot="title"><i class="el-icon-check"></i>报表中心</template>
                <el-menu-item index="beibei_milk_powder">贝贝奶粉报表</el-menu-item>
            </el-submenu>
            <el-submenu index="2">
                <template slot="title"><i class="el-icon-check"></i>验证中心</template>
                <el-menu-item index="create_validation">单个验证</el-menu-item>
                <el-menu-item index="create_batch_validation">提交批量验证</el-menu-item>
                <el-menu-item index="batch_validation_list">批量验证列表</el-menu-item>
            </el-submenu>
            <el-submenu index="3">
                <template slot="title"><i class="el-icon-menu"></i>算法中心</template>
                <el-menu-item index="create_algorithm">新建算法</el-menu-item>
                <el-menu-item index="algorithm_list">算法列表</el-menu-item>
            </el-submenu>
            <el-submenu index="4">
                <template slot="title"><i class="el-icon-document"></i>模型中心</template>
                <el-menu-item index="create_model">新建模型</el-menu-item>
                <el-menu-item index="model_list">模型列表</el-menu-item>
            </el-submenu>
            <el-submenu index="5">
                <template slot="title"><i class="el-icon-information"></i>数据集中心</template>
                <el-menu-item index="create_trainset">新建训练集</el-menu-item>
                <el-menu-item index="trainset_list">训练集列表</el-menu-item>
                <el-menu-item index="create_testset">新建测试集</el-menu-item>
                <el-menu-item index="testset_list">测试集列表</el-menu-item>
            </el-submenu>
            <el-submenu index="6">
                <template slot="title"><i class="el-icon-star-on"></i>数据统计</template>
                <el-menu-item index="basecharts">基础图表</el-menu-item>
                <el-menu-item index="mixcharts">混合图表</el-menu-item>
                <el-menu-item index="vueeditor">编辑器</el-menu-item>
                <el-menu-item index="markdown">markdown</el-menu-item>
                <el-menu-item index="upload">文件上传</el-menu-item>
            </el-submenu>
            <el-submenu index="7">
                <template slot="title"><i class="el-icon-setting"></i>设置</template>
                <el-menu-item index="create_user">创建用户</el-menu-item>
                <el-menu-item index="user_list">用户列表</el-menu-item>
            </el-submenu>
        </el-menu>
    </div>
</template>

<script>
    export default {
        computed:{
            onRoutes(){
                return this.$route.path.replace('/','');
            }
        }
    }
</script>

<style scoped>
    .sidebar{
        display: block;
        position: absolute;
        width: 250px;
        left: 0;
        top: 70px;
        bottom:0;
        background: #2E363F;
    }
    .sidebar > ul {
        height:100%;
    }
</style>
