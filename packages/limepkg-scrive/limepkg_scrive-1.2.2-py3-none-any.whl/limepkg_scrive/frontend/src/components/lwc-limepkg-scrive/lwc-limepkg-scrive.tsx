import {
    LimeWebComponent,
    LimeWebComponentContext,
    LimeWebComponentPlatform,
    NotificationService,
    PlatformServiceName,
    LimeobjectsStateService
} from '@limetech/lime-web-components-interfaces';
import { Component, Element, h, Prop, State } from '@stencil/core';
import { Configs, CurrentLimeobject, Session } from '@limetech/lime-web-components-decorators';
import { ListItem, ListSeparator, ValidationStatus, Tab } from '@limetech/lime-elements';

type File = {
    extension: string,
    filename: string,
    size: number;
}

@Component({
    tag: 'lwc-limepkg-scrive',
    shadow: true,
    styleUrl: 'lwc-limepkg-scrive.scss',
})
export class Test implements LimeWebComponent {

    @CurrentLimeobject()
    @State()
    private document: any = {}

    @Session()
    @State()
    private session: any = {};

    @Prop()
    public platform: LimeWebComponentPlatform;

    @Configs({})
    @State()
    private config: any = {}

    @Prop()
    public context: LimeWebComponentContext;

    @Element()
    public element: HTMLElement;

    @State()
    public includePerson = true;
    @State()
    public includeCoworker = true;
    @State()
    private cloneDocument = true;


    private goToScrive(id) {
        const host = this.config.limepkg_scrive.scriveHost;
        const lang = this.session.language;
        window.open(`${host}/public/?limeDocId=${id}&lang=${lang}&usePerson=${this.includePerson}&useCoworker=${this.includeCoworker}&cloneDocument=${this.cloneDocument}`);
    }


    private files(): File[] {
        const fileMap = this.document?._files || {};
        const fileIds = Object.keys(fileMap);
        return fileIds.map(id => fileMap[id]);
    }

    private allowedExtensions = Object.freeze(["PDF", "DOC", "DOCX"]);
    private isSignable(file: File): boolean {
        return this.allowedExtensions.includes((file.extension || "").toUpperCase())
    }

    private setCloneDocument = (event: CustomEvent<boolean>) => {
        event.stopPropagation();
        this.cloneDocument = event.detail;
    };

    public render() {
        if (this.context.limetype !== 'document') {
            return;
        }

        const signableFiles = this.files().filter(this.isSignable, this);
        const noSignableFiles = signableFiles.length === 0;
        const tooManySignableFiles = signableFiles.length > 1
        if (noSignableFiles || tooManySignableFiles) {
            return;
        }

        const translate = this.platform.get(PlatformServiceName.Translate);
        const label = translate.get("limepkg_scrive.primary_action")
        const cloneLabel = translate.get("limepkg_scrive.clone_document")
        const cloneWarning = translate.get("limepkg_scrive.clone_warning")

        return (
            <section>
                <limel-config config={{ iconPath: '/static/limepkg_scrive/static/' }} />
                <limel-button
                    label={label}
                    outlined={true}
                    icon="scrive"
                    onClick={() =>
                        this.goToScrive(this.context.id)
                    }
                />
                <limel-checkbox
                    label={cloneLabel}
                    checked={this.cloneDocument}
                    onChange={this.setCloneDocument}
                />
                <p>{cloneWarning}</p>
            </section>
        );
    }
}
