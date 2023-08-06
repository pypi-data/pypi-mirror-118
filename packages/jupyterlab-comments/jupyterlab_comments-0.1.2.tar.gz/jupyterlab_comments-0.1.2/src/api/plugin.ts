import {
  ILabShell,
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { WidgetTracker } from '@jupyterlab/apputils';
import { CommentPanel } from './panel';
import { CommentWidget } from './widget';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { CommentRegistry, CommentWidgetRegistry } from './registry';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { DocumentRegistry, DocumentWidget } from '@jupyterlab/docregistry';
import { Menu } from '@lumino/widgets';
import { CommentFileModelFactory } from './model';
import {
  ICommentPanel,
  ICommentRegistry,
  ICommentWidgetRegistry
} from './token';

namespace CommandIDs {
  export const addComment = 'jl-comments:add-comment';
  export const deleteComment = 'jl-comments:delete-comment';
  export const editComment = 'jl-comments:edit-comment';
  export const replyToComment = 'jl-comments:reply-to-comment';
  export const save = 'jl-comments:save';
}

export type CommentTracker = WidgetTracker<CommentWidget<any>>;

/**
 * A plugin that provides a `CommentRegistry`
 */
export const commentRegistryPlugin: JupyterFrontEndPlugin<ICommentRegistry> = {
  id: 'jupyterlab-comments:comment-registry',
  autoStart: true,
  provides: ICommentRegistry,
  activate: (app: JupyterFrontEnd) => {
    return new CommentRegistry();
  }
};

/**
 * A plugin that provides a `CommentWidgetRegistry`
 */
export const commentWidgetRegistryPlugin: JupyterFrontEndPlugin<ICommentWidgetRegistry> =
  {
    id: 'jupyterlab-comments:comment-widget-registry',
    autoStart: true,
    provides: ICommentWidgetRegistry,
    activate: (app: JupyterFrontEnd) => {
      return new CommentWidgetRegistry();
    }
  };

export const jupyterCommentingPlugin: JupyterFrontEndPlugin<ICommentPanel> = {
  id: 'jupyterlab-comments:commenting-api',
  autoStart: true,
  requires: [
    ICommentRegistry,
    ICommentWidgetRegistry,
    ILabShell,
    IDocumentManager,
    IRenderMimeRegistry
  ],
  provides: ICommentPanel,
  activate: (
    app: JupyterFrontEnd,
    commentRegistry: ICommentRegistry,
    commentWidgetRegistry: ICommentWidgetRegistry,
    shell: ILabShell,
    docManager: IDocumentManager,
    renderer: IRenderMimeRegistry
  ): CommentPanel => {
    const filetype: DocumentRegistry.IFileType = {
      contentType: 'file',
      displayName: 'comment',
      extensions: ['.comment'],
      fileFormat: 'json',
      name: 'comment',
      mimeTypes: ['application/json']
    };

    const commentTracker = new WidgetTracker<CommentWidget<any>>({
      namespace: 'comment-widgets'
    });

    const panel = new CommentPanel({
      commands: app.commands,
      commentRegistry,
      commentWidgetRegistry,
      docManager,
      shell,
      renderer
    });

    // Create the directory holding the comments.
    void panel.pathExists(panel.pathPrefix).then(exists => {
      const contents = docManager.services.contents;
      if (!exists) {
        void contents
          .newUntitled({
            path: '/',
            type: 'directory'
          })
          .then(model => {
            void contents.rename(model.path, panel.pathPrefix);
          });
      }
    });

    addCommands(app, commentTracker, panel);

    const commentMenu = new Menu({ commands: app.commands });
    commentMenu.addItem({ command: CommandIDs.deleteComment });
    commentMenu.addItem({ command: CommandIDs.editComment });
    commentMenu.addItem({ command: CommandIDs.replyToComment });

    app.contextMenu.addItem({
      command: CommandIDs.deleteComment,
      selector: '.jc-Comment'
    });
    app.contextMenu.addItem({
      command: CommandIDs.editComment,
      selector: '.jc-Comment'
    });
    app.contextMenu.addItem({
      command: CommandIDs.replyToComment,
      selector: '.jc-Comment'
    });

    const modelFactory = new CommentFileModelFactory({
      commentRegistry,
      commentWidgetRegistry,
      commentMenu
    });

    app.docRegistry.addFileType(filetype);
    app.docRegistry.addModelFactory(modelFactory);

    // Add the panel to the shell's right area.
    shell.add(panel, 'right', { rank: 600 });

    // Load model for current document when it changes
    shell.currentChanged.connect((_, args) => {
      if (args.newValue != null && args.newValue instanceof DocumentWidget) {
        const docWidget = args.newValue as DocumentWidget;
        docWidget.context.ready
          .then(() => {
            void panel.loadModel(docWidget.context);
          })
          .catch(() => {
            console.warn('Unable to load panel');
          });
      }
    });

    // Update comment widget tracker when model changes
    panel.modelChanged.connect((_, fileWidget) => {
      if (fileWidget != null) {
        fileWidget.widgets.forEach(
          widget => void commentTracker.add(widget as CommentWidget<any>)
        );
        fileWidget.commentAdded.connect(
          (_, commentWidget) => void commentTracker.add(commentWidget)
        );
      }
    });

    // Reveal the comment panel when a comment is added.
    panel.commentAdded.connect((_, comment) => {
      const identity = comment.identity;

      // If you didn't make the comment, ignore it
      // Comparing ids would be better but they're not synchronized across Docs/awarenesses
      if (identity == null || identity.name !== panel.localIdentity.name) {
        return;
      }

      // Automatically opens panel when a document with comments is opened,
      // or when the local user adds a new comment
      if (!panel.isVisible) {
        shell.activateById(panel.id);
        if (comment.text === '') {
          comment.openEditActive();
        }
      }

      panel.scrollToComment(comment.id);
    });

    app.contextMenu.addItem({
      command: CommandIDs.save,
      selector: '.jc-CommentPanel'
    });

    return panel;
  }
};

function addCommands(
  app: JupyterFrontEnd,
  commentTracker: CommentTracker,
  panel: ICommentPanel
): void {
  app.commands.addCommand(CommandIDs.save, {
    label: 'Save Comments',
    execute: () => {
      const fileWidget = panel.fileWidget;
      if (fileWidget == null) {
        return;
      }

      void fileWidget.context.save();
    }
  });

  app.commands.addCommand(CommandIDs.deleteComment, {
    label: 'Delete Comment',
    execute: () => {
      const currentComment = commentTracker.currentWidget;
      if (currentComment != null) {
        currentComment.deleteActive();
      }
    }
  });

  app.commands.addCommand(CommandIDs.editComment, {
    label: 'Edit Comment',
    execute: () => {
      const currentComment = commentTracker.currentWidget;
      if (currentComment != null) {
        currentComment.openEditActive();
      }
    }
  });

  app.commands.addCommand(CommandIDs.replyToComment, {
    label: 'Reply to Comment',
    execute: () => {
      const currentComment = commentTracker.currentWidget;
      if (currentComment != null) {
        currentComment.revealReply();
      }
    }
  });
}

const plugins: JupyterFrontEndPlugin<any>[] = [
  jupyterCommentingPlugin,
  commentRegistryPlugin,
  commentWidgetRegistryPlugin
];

export default plugins;
