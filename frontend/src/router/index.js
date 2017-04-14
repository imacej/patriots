import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [{
            path: '/',
            redirect: '/login'
        },
        {
            path: '/home',
            component: resolve => require(['../components/common/Home.vue'], resolve),
            children: [{
                    path: '/',
                    redirect: 'readme'
                },
                {
                    path: 'readme',
                    component: resolve => require(['../components/page/Readme.vue'], resolve)
                },
                // 全新设计
                {
                    path: 'beibei_milk_powder',
                    component: resolve => require(['../components/page/report/BBMilkPowder.vue'], resolve)
                },
                // FORM 用来新建各种数据
                {
                    path: 'create_trainset',
                    component: resolve => require(['../components/page/form/Trainset.vue'], resolve)
                },
                {
                    path: 'create_testset',
                    component: resolve => require(['../components/page/form/Testset.vue'], resolve)
                },
                {
                    path: 'create_model',
                    component: resolve => require(['../components/page/form/Model.vue'], resolve)
                },
                {
                    path: 'create_algorithm',
                    component: resolve => require(['../components/page/form/Algorithm.vue'], resolve)
                },
                {
                    path: 'create_validation',
                    component: resolve => require(['../components/page/form/Validation.vue'], resolve)
                },
                {
                    path: 'create_batch_validation',
                    component: resolve => require(['../components/page/form/BatchValidation.vue'], resolve)
                },
                {
                    path: 'create_user',
                    component: resolve => require(['../components/page/form/User.vue'], resolve)
                },
                // Table 项目列表
                {
                    path: 'trainset_list',
                    component: resolve => require(['../components/page/table/Trainset.vue'], resolve)
                },
                {
                    path: 'testset_list',
                    component: resolve => require(['../components/page/table/Testset.vue'], resolve)
                },
                {
                    path: 'algorithm_list',
                    component: resolve => require(['../components/page/table/Algorithm.vue'], resolve)
                },
                {
                    path: 'model_list',
                    component: resolve => require(['../components/page/table/Model.vue'], resolve)
                },
                {
                    path: 'batch_validation_list',
                    component: resolve => require(['../components/page/table/BatchValidation.vue'], resolve)
                },
                {
                    path: 'user_list',
                    component: resolve => require(['../components/page/table/User.vue'], resolve)
                },

                {
                    path: 'basetable',
                    component: resolve => require(['../components/page/other/BaseTable.vue'], resolve)
                },
                {
                    path: 'baseform',
                    component: resolve => require(['../components/page/other/BaseForm.vue'], resolve)
                },
                {
                    path: 'settings',
                    component: resolve => require(['../components/page/Settings.vue'], resolve) // vue-echarts-v3组件
                },
                {
                    path: 'vueeditor',
                    component: resolve => require(['../components/page/other/VueEditor.vue'], resolve) // Vue-Quill-Editor组件
                },
                {
                    path: 'markdown',
                    component: resolve => require(['../components/page/other/Markdown.vue'], resolve) // Vue-Quill-Editor组件
                },
                {
                    path: 'upload',
                    component: resolve => require(['../components/page/other/Upload.vue'], resolve) // Vue-Core-Image-Upload组件
                },
                {
                    path: 'basecharts',
                    component: resolve => require(['../components/page/other/BaseCharts.vue'], resolve) // vue-echarts-v3组件
                },
                {
                    path: 'mixcharts',
                    component: resolve => require(['../components/page/other/MixCharts.vue'], resolve) // vue-echarts-v3组件
                },
                {
                    path: '*', //其他页面，强制跳转到登录页面
                    redirect: '/login'
                }
            ]
        },
        {
            path: '/login',
            component: resolve => require(['../components/page/Login.vue'], resolve)
        },
    ]
})