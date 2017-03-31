import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [{
            path: '/',
            redirect: '/login'
        },
        {
            path: '/readme',
            component: resolve => require(['../components/common/Home.vue'], resolve),
            children: [{
                    path: '/',
                    component: resolve => require(['../components/page/Readme.vue'], resolve)
                },
                {
                    path: '/basetable',
                    component: resolve => require(['../components/page/BaseTable.vue'], resolve)
                },
                {
                    path: '/vuetable',
                    component: resolve => require(['../components/page/VueTable.vue'], resolve) // vue-datasource组件
                },
                {
                    path: '/baseform',
                    component: resolve => require(['../components/page/BaseForm.vue'], resolve)
                },
                {
                    path: '/createdataset',
                    component: resolve => require(['../components/page/FormCreateDataset.vue'], resolve)
                },
                {
                    path: '/createmodel',
                    component: resolve => require(['../components/page/FormCreateModel.vue'], resolve)
                },
                {
                    path: '/createalgo',
                    component: resolve => require(['../components/page/FormCreateAlgorithm.vue'], resolve)
                },
                {
                    path: '/createtest',
                    component: resolve => require(['../components/page/FormCreateTest.vue'], resolve)
                },
                {
                    path: '/createbatchtest',
                    component: resolve => require(['../components/page/FormCreateBatchTest.vue'], resolve)
                },
                {
                    path: '/datasetlist',
                    component: resolve => require(['../components/page/TableDataset.vue'], resolve)
                },
                {
                    path: '/algolist',
                    component: resolve => require(['../components/page/TableAlgorithm.vue'], resolve)
                },
                {
                    path: '/modellist',
                    component: resolve => require(['../components/page/TableModel.vue'], resolve)
                },
                {
                    path: '/batchtestlist',
                    component: resolve => require(['../components/page/TableBatchTest.vue'], resolve)
                },
                {
                    path: '/settings',
                    component: resolve => require(['../components/page/Settings.vue'], resolve) // vue-echarts-v3组件
                },
                {
                    path: '/vueeditor',
                    component: resolve => require(['../components/page/VueEditor.vue'], resolve) // Vue-Quill-Editor组件
                },
                {
                    path: '/markdown',
                    component: resolve => require(['../components/page/Markdown.vue'], resolve) // Vue-Quill-Editor组件
                },
                {
                    path: '/upload',
                    component: resolve => require(['../components/page/Upload.vue'], resolve) // Vue-Core-Image-Upload组件
                },
                {
                    path: '/basecharts',
                    component: resolve => require(['../components/page/BaseCharts.vue'], resolve) // vue-echarts-v3组件
                },
                {
                    path: '/mixcharts',
                    component: resolve => require(['../components/page/MixCharts.vue'], resolve) // vue-echarts-v3组件
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