import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { AppService } from '../app.service';
import { Usuario } from '../models/usuario.model';

@Component({
    selector: 'app-funcionarios',
    templateUrl: './funcionarios.component.html',
    styleUrls: ['./funcionarios.component.scss']
})

export class FuncionariosComponent implements OnInit {
    @Input() userData!: Usuario;

    /**
     * Grids
     */
    @ViewChild(MatSort, { static: true }) gridSort!: MatSort;
    @ViewChild(MatPaginator, { static: true }) gridPaginator!: MatPaginator;
 
    private data: Array<Usuario> = [];
    public componentIsLoading: boolean = true;

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
    public modalUser: string = '';
    public modalEmail: string = '';
    public modalSenha: string = '';
    public modalHidePassword: boolean = true;

    constructor(
        private appService: AppService,
        private snackBar: MatSnackBar) { }

    ngOnInit() {
        this.gridData.sort = this.gridSort;
        this.gridData.paginator = this.gridPaginator;
        this.getData();
    }

    /**
     * Função responsável por obter os dados
     */
    public async getData() {
        this.componentIsLoading = true;
        
        if (this.data.length === 0) {
            this.data = await this.appService.getFuncionarios();
        }

        this.componentIsLoading = false;

        this.gridData.data = this.data;
        this.gridColumns = [
            { name: '_id', display: 'Matrícula' },
            { name: 'nome', display: 'Nome' },
            { name: 'usuario', display: 'Usuário' },
            { name: 'email', display: 'Email' },
            { name: 'cargo', display: 'Cargo' }
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
                title: 'Adicionar um funcionário',
                role: 'add'
            };

            this.showModal = true;
        }
        else {
            this.modal = {
                title: 'Editar dados do funcionário',
                role: 'edit'
            };
    
            const funcionario = this.data.filter(e => e._id === id)[0];
    
            this.modalId = id;
            this.modalNome = funcionario.nome;
            this.modalUser = funcionario.usuario;
            this.modalEmail = funcionario.email;
            this.modalSenha = '';
    
            this.showModal = true;
        }
    }

    /**
     * Função responsável por ocultar a modal
     */
    public hideModal() {
        this.modalId = '';
        this.modalNome = '';
        this.modalUser = '';
        this.modalEmail = '';
        this.modalSenha = '';
        this.modalHidePassword = true;

        this.showModal = false;
    }

    /**
     * Botão de remoção do grid
     */
    public async gridControlRemoveClick(id: string) {
        const data: any = await this.appService.removeFuncionario(id);
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
            data = await this.appService.addFuncionario(this.modalNome, this.modalUser, this.modalEmail, this.modalSenha);
            
            if (data.hasOwnProperty('status')) {
                message = data.error.message;
            }
            else {
                message = data.message;
            }
        }
        else {
            data = await this.appService.editFuncionario(this.modalId, this.modalNome, this.modalUser, this.modalEmail, this.modalSenha);
            
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
