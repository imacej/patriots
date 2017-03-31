<template>
    <div class="sidebar">
        <el-menu :default-active="onRoutes" class="el-menu-vertical-demo" theme="dark" unique-opened router>
            <el-menu-item index="readme">
                <i class="el-icon-view"></i>系统概况
            </el-menu-item>
            <el-submenu index="1">
                <template slot="title"><i class="el-icon-check"></i>测试中心</template>
                <el-menu-item index="createtest">单个测试</el-menu-item>
                <el-menu-item index="createbatchtest">提交批量测试</el-menu-item>
                <el-menu-item index="batchtestlist">批量测试列表</el-menu-item>
            </el-submenu>
            <el-submenu index="2">
                <template slot="title"><i class="el-icon-menu"></i>算法中心</template>
                <el-menu-item index="createalgo">新建算法</el-menu-item>
                <el-menu-item index="algolist">算法列表</el-menu-item>
            </el-submenu>
            <el-submenu index="3">
                <template slot="title"><i class="el-icon-document"></i>模型中心</template>
                <el-menu-item index="createmodel">新建模型</el-menu-item>
                <el-menu-item index="modellist">模型列表</el-menu-item>
                
            </el-submenu>
            <el-submenu index="4">
                <template slot="title"><i class="el-icon-information"></i>数据集中心</template>
                <el-menu-item index="createdataset">新建数据集</el-menu-item>
                <el-menu-item index="datasetlist">数据集列表</el-menu-item>
            </el-submenu>
            <el-submenu index="5">
                <template slot="title"><i class="el-icon-star-on"></i>数据统计</template>
                <el-menu-item index="basecharts">基础图表</el-menu-item>
                <el-menu-item index="mixcharts">混合图表</el-menu-item>
                <el-menu-item index="vueeditor">编辑器</el-menu-item>
                <el-menu-item index="markdown">markdown</el-menu-item>
                <el-menu-item index="upload">文件上传</el-menu-item>
            </el-submenu>
            <el-menu-item index="settings">
                <i class="el-icon-setting"></i>系统设置
            </el-menu-item>
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
