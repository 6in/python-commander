Ext.define('Pages.MonacoSampleViewModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.MonacoSample',
    data: {
        text: 'sample',
        original: 'This line is removed on the right.\njust some text\nabcd\nefgh\nSome more text',
        modified: 'just some text\nabcz\nzzzzefgh\nSome more text.\nThis line is removed on the left.'
    },
    stores: {
        sampleStore: {
            fields: [
                { name: 'name', type: 'string' },
                { name: 'age', type: 'int' }
            ],
            data: [
                { name: 'HTML', age: 29 },
                { name: 'javascript', age: 23 },
                { name: 'C', age: 46 }
            ]
        }
    }
});

Ext.define('Page.MonacoSampleController', {
    extend: 'Pages.BaseController',
    alias: 'controller.MonacoSample',
    init() {
        const me = this
        me.callParent(arguments)
    },
    onClickOk() {
        const me = this
        const text = me.getViewModel().getData().text;
        const diff = me.lookupReference('diff')
        diff.setOriginal(text);
    }
});

Ext.define('Pages.MonacoSample', {
    extend: 'Ext.panel.Panel',

    controller: 'MonacoSample',
    viewModel: 'MonacoSample',

    title: 'Monaco-Panel',

    layout: 'border',

    items: [{
        region: 'north',
        split: true,
        height: 300,
        layout: 'fit',
        items: {
            xtype: 'monaco',
            options: {
                language: 'javascript',
                minimap: {
                    enabled: true
                }
            },
            bind: {
                value: '{text}',
            },
        },
        buttons: [{
            text: 'OK',
            handler: 'onClickOk'
        }]
    }, {
        region: 'center',
        reference: 'diff',
        title: 'diff sample',
        layout: 'fit',
        items: {
            xtype: 'monacodiff',
            bind: {
                original: '{original}',
                modified: '{modified}'
            }
        }
    }, {
        region: 'south',
        title: 'grid sample',
        split: true,
        height: 300,
        layout: 'fit',
        xtype: 'grid',
        plugins: [
            { ptype: 'cellediting', clicksToEdit: 1 },
            { ptype: 'clipboard' }
        ],
        columnLines: true,
        selModel: {
            type: 'spreadsheet',
            columnSelect: true
        },
        columns: [
            { xtype: 'rownumberer', width: 60, header: 'No.' },
            { header: 'name', dataIndex: 'name' },
            { header: 'age', dataIndex: 'age' }
        ],
        bind: '{sampleStore}',
    }]
});