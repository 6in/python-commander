Ext.application({
    name: 'extjs cdn base application',

    launch() {
        Ext.Loader.setPath('Pages', './Pages');
        Ext.Loader.setConfig({
            enabled: true
        });

        new Promise((resolve, reject) => {
            // Monacoエディタのロードを先に行う
            require(['vs/editor/editor.main'], () => {
                resolve()
            })
        }).then((respose) => {
            // あらかじめロードするページ一覧
            const pages = [
                'Pages.BaseController',
                'Pages.MainMenu',
                'Pages.components.TemplateComponent',
                'Pages.components.Monaco',
                'Pages.components.MonacoDiff',
                'Pages.components.Iframe',
                'Pages.components.HandsonTable',
                'Pages.components.Markdown',
            ]
            // ページをロードする
            Ext.require(pages, this.createViewPort);
        })
    },
    createViewPort() {
        // ロード完了後、ビューポートを作成
        Ext.create('Ext.Viewport', {
            renderTo: document.body,
            layout: 'border',
            itemId: 'viewport',
            items: [{
                region: 'west',
                title: 'Home',
                iconCls: 'fa fa-home',
                collapsible: true,
                split: true,
                width: 400,
                xtype: 'mainmenu'
            }, {
                region: 'center',
                layout: 'fit',
                xtype: 'tabpanel',
                itemId: 'targetPage'
            }]
        });
    }
});