Ext.define('Pages.components.Monaco', {
    extend: 'Ext.Component',
    alias: 'widget.monaco',
    config: {
        value: '',
        theme: 'vs-dark',
        tabSize: 2,
        fontSize: 14,
        automaticLayout: true,
        language: '',
        options: {}
    },
    twoWayBindable: [
        'value'
    ],
    renderTpl: '<div id="{id}_monaco" style="width:100%;height:100%"></div>',
    constructor(config) {
        this.callParent([config])
        return
    },
    initComponent() {
    },
    getValue() {
        if (this.editor) {
            return this.editor.getValue();
        }
        return '';
    },
    setValue(text) {
        if (this.editor) {
            if (this.editor.getValue() !== text) {
                this.editor.setValue(text);
            }
        }
        this.callParent([text])
    },
    listeners: {
        afterrender() {
            const me = this
            const id = `${me.getId()}_monaco`
            me.targetDiv = document.getElementById(id)
            const options = Object.assign(
                {
                    value: me.getValue(),
                    automaticLayout: me.getAutomaticLayout(),
                    fontSize: me.getFontSize(),
                    tabSize: me.getTabSize(),
                    theme: me.getTheme(),
                    language: me.getLanguage()
                },
                me.getOptions())

            me.editor = monaco.editor.create(me.targetDiv, options);
            me.editor.onDidChangeModelContent(event => {
                const value = me.editor.getValue();
                me.fireEvent('change', me, [me.editor.getValue()]);
                me.setValue(value);
            });
        },
        resize(obj, width, height) {
            const me = this
            if (me.editor) {
                me.editor.layout();
            }
        }
    },
    monaco() {
        const me = this;
        if (me.editor) {
            return me.editor
        }
        return null;
    }
});
