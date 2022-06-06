import { Component, Input, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatTableDataSource } from '@angular/material/table';
import { AppService } from '../app.service';
import { Projeto } from '../models/projetos.model';
import { Usuario } from '../models/usuario.model';

@Component({
    selector: 'app-projetos',
    templateUrl: './projetos.component.html',
    styleUrls: ['./projetos.component.scss']
})

export class ProjetosComponent implements OnInit {
    @Input() userData!: Usuario;

    /**
     * Grids
     */
    public seusProjetosData: Array<Projeto> = [];
    public data: Array<Projeto> = [];
    public componentIsLoading: boolean = true;

    public gridProjetosUserData: MatTableDataSource<any> = new MatTableDataSource();
    public gridProjetosUserColumns: Array<any> = [];
    public gridProjetosUserColumnsToDisplay: Array<string> = [];

    public gridData: MatTableDataSource<any> = new MatTableDataSource();
    public gridColumns: Array<any> = [];
    public gridColumnsToDisplay: Array<string> = [];

    /**
     * Modal
     */
    public showModal: boolean = false;
    public modal: any = {};
    public modalId: string = '';
    public modalNome: string = '';
    public modalDescricao: string = '';
    public modalParticipante: string = '';

    constructor(
        private appService: AppService,
        private snackBar: MatSnackBar) { }

    ngOnInit() {
        this.getUserData();
        this.getData();
    }

    /**
     * Função responsável por obter os dados
     */
    private async getUserData() {
        if (this.seusProjetosData.length === 0) {
            this.seusProjetosData = await this.appService.getProjetosUserLogado();
        }

        for (const projeto of this.seusProjetosData) {
            projeto.suaCargaHoraria = `${projeto.participantes.filter(e => e.matricula === this.userData._id)[0].cargaHorariaSemanal} horas`;
        }

        this.gridProjetosUserData.data = this.seusProjetosData;
        this.gridProjetosUserColumns = [
            { name: '_id', display: 'Identificador' },
            { name: 'nome', display: 'Nome' },
            { name: 'dataInicio', display: 'Data de início' },
            { name: 'dataFim', display: 'Previsão de término' },
            { name: 'suaCargaHoraria', display: 'Sua carga horária semanal' }
        ];

        this.gridProjetosUserColumnsToDisplay = this.gridProjetosUserColumns.map(col => col.name);
    }

    /**
     * Função responsável por obter os dados
     */
    private async getData() {
        this.componentIsLoading = true;

        if (this.data.length === 0) {
            this.data = await this.appService.getProjetos();
        }

        this.componentIsLoading = false;

        this.gridData.data = this.data;
        this.gridColumns = [
            { name: 'nome', display: 'Nome' },
            { name: 'descricao', display: 'Descrição' },
            { name: 'dataInicio', display: 'Data de início' },
            { name: 'dataFim', display: 'Previsão de término' },
            { name: 'participantes', display: 'Participantes' },
        ];

        if (this.userData.possuiPermissaoRH) {
            this.gridColumns.push({ name: 'controls', display: 'Ações' });
        }

        this.gridColumnsToDisplay = this.gridColumns.map(col => col.name);
    }

    /**
     * Função responsável por abrir a modal
     */
    public openModal(id: string = '') {
        if (id === '') {
            this.modal = {
                title: 'Adicionar um projeto',
                role: 'add'
            };

            this.showModal = true;
        }
        else {
            this.modal = {
                title: 'Editar o projeto',
                role: 'edit'
            };

            const projeto = this.data.filter(e => e._id === id)[0];

            this.modalId = id;
            this.modalNome = projeto.nome;
            this.modalDescricao = projeto.descricao;
            this.modalParticipante = projeto.participantes[0].email;

            this.showModal = true;
        }
    }

    /**
     * Função responsável por ocultar a modal
     */
    public hideModal() {
        this.modalId = '';
        this.modalNome = '';
        this.modalDescricao = '';
        this.modalParticipante = '';

        this.showModal = false;
    }

    /**
     * Botão de remoção do grid
     */
    public async gridControlRemoveClick(id: string) {
        const data: any = await this.appService.removeProjeto(id);
        let message;

        if (data.hasOwnProperty('status')) {
            message = data.error.message;
        }
        else {
            message = data.message;
        }

        this.data = [];
        this.snackBar.open(message, 'Fechar');
        this.getData();
    }

    /**
     * Ação da modal
     */
    public async actionModal(role: 'add' | 'edit') {
        let message: string;
        let data: any;

        if (role === 'add') {
            data = await this.appService.addProjeto(this.modalNome, this.modalDescricao, [this.modalParticipante]);

            if (data.hasOwnProperty('status')) {
                message = data.error.message;
            }
            else {
                message = data.message;
            }
        }
        else {
            data = await this.appService.editProjeto(this.modalId, this.modalNome, this.modalDescricao, [this.modalParticipante]);

            if (data.hasOwnProperty('status')) {
                message = data.error.message;
            }
            else {
                message = data.message;
            }
        }

        this.hideModal();
        this.snackBar.open(message, 'Fechar');
        this.data = [];
        this.getData();
    }
}
