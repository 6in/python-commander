Ext.define('Pages.components.MonacoDiff', {
    extend: 'Ext.Component',
    alias: 'widget.monacodiff',
    config: {
        original: '',
        modified: '',
        options: {}
    },
    renderTpl: '<div id="{id}_monacodiff" style="width:100%;height:100%"></div>',
    constructor(config) {
        this.callParent([config])
        return
    },
    initComponent() {
    },
    setOriginal(text) {
        this.callParent([text])
        this.setModel()
    },
    setModified(text) {
        this.callParent([text])
        this.setModel()
    },
    setModel() {
        const me = this
        if (!me.editor) {
            return;
        }
        var originalModel = monaco.editor.createModel(me.getOriginal());
        var modifiedModel = monaco.editor.createModel(me.getModified());
        me.editor.setModel({
            original: originalModel,
            modified: modifiedModel
        });
    },
    listeners: {
        afterrender() {
            const me = this
            const id = `${me.getId()}_monacodiff`
            me.targetDiv = document.getElementById(id)
            const options = Object.assign({},
                me.getOptions());

            me.editor = monaco.editor.createDiffEditor(me.targetDiv, options);
            me.setModel()
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
