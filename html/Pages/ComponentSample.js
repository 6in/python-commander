Ext.define('Pages.ComponentSampleViewModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.ComponentSample',
    data: {
        title: 'Sample Components',
        url: '',
        komazawa: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3243.1897762780477!2d139.66157770469536!3d35.62304777643898!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x6018f4f2bc54ffab%3A0x6e427037e4c90f2d!2z6YO956uL6aeS5rKi44Kq44Oq44Oz44OU44OD44Kv5YWs5ZyS!5e0!3m2!1sja!2sjp!4v1582419108483!5m2!1sja!2sjp',
        yoyogi: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2291.9254440540626!2d139.69493842532367!3d35.670302840385055!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x60188cb479620a33%3A0x34bcc78ce7f8bf3e!2z5Luj44CF5pyo5YWs5ZyS!5e0!3m2!1sja!2sjp!4v1582456324431!5m2!1sja!2sjp',
        rows: [
            [1, 2, 3, 4],
            [1, 2, 3, 4],
        ],
        markdown: `
Marked - Markdown Parser
========================

[Marked] lets you convert [Markdown] into HTML.  Markdown is a simple text format whose goal is to be very easy to read and write, even when not converted to HTML.  This demo page will let you type anything you like and see how it gets converted.  Live.  No more waiting around.

How To Use The Demo
-------------------

1. Type in stuff on the left.
2. See the live updates on the right.

That's it.  Pretty simple.  There's also a drop-down option in the upper right to switch between various views:

- **Preview:**  A live display of the generated HTML as it would render in a browser.
- **HTML Source:**  The generated HTML before your browser makes it pretty.
- **Lexer Data:**  What [marked] uses internally, in case you like gory stuff like this.
- **Quick Reference:**  A brief run-down of how to format things using markdown.

[Marked]: https://github.com/markedjs/marked/
[Markdown]: http://daringfireball.net/projects/markdown/
    `
    }
});

Ext.define('Page.ComponentSampleController', {
    extend: 'Pages.BaseController',
    alias: 'controller.ComponentSample',
    init() {
        const me = this
        me.callParent(arguments)
    },
    onChangeMap(obj) {
        const me = this;
        const data = me.getViewModel().getData()
        me.getViewModel().setData({
            url: data[obj.text]
        });
    },
    onGetGridData() {
        const me = this;
        const grid = me.lookupReference('grid');

        console.log(grid.getData());

        console.log(me.getViewModel().getData().rows);
    }
});

Ext.define('Pages.ComponentSample', {
    extend: 'Ext.panel.Panel',

    controller: 'ComponentSample',
    viewModel: 'ComponentSample',

    // iconCls: 'fa fa-ambulance',

    bind: {
        title: '{title}'
    },

    layout: {
        type: 'vbox',
        align: 'stretch',
        pack: 'start'
    },

    items: [
        {
            tbar: [
                { text: 'komazawa', handler: 'onChangeMap' },
                { text: 'yoyogi', handler: 'onChangeMap' },
            ],
            title: 'iframe',
            layout: 'fit',
            flex: 0.1,
            items: {
                xtype: 'iframe',
                bind: {
                    src: '{url}'
                },
            }
        },
        {
            flex: 0.1,
            title: 'handson-table sample',
            layout: 'fit',
            tbar: [
                { text: 'Get data', handler: 'onGetGridData' }
            ],
            items: {
                xtype: 'handson-table',
                reference: 'grid',
                // rows: [[1, 2], [1, 2]],
                bind: {
                    data: '{rows}'
                }
            }
        },
        {
            flex: 0.1,
            title: 'Markdown',
            layout: 'fit',
            items: {
                xtype: 'markdown',
                bind: {
                    value: '{markdown}'
                }
            }
        },
    ]

});