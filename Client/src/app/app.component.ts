import { Component, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { AppService } from './app.service';
import { Login } from './models/login.model';
import { Projeto } from './models/projetos.model';
import { Usuario } from './models/usuario.model';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})

export class AppComponent {
    /**
     * Controla se o usuario esta logado
     */
    public userIsLogged: boolean = false;
    public userLoginData: string = '';
    public userData: Usuario;

    /**
     * Controla a exibicao da modal de login
     */
    public showLogin: boolean = false;
    public hidePassword: boolean = true;

    /**
     * Variaveis para o login
     */
    public formLoginEmail = '';
    public formLoginSenha = '';

    /**
     * Variáveis para controle do item sendo exibido
     */
    public componentInView: 'PROJETOS' | 'FUNCIONARIOS' = 'FUNCIONARIOS';
    public componentIsLoading: boolean = true;

    /**
     * Variáveis para exibição dos dados
     */
    public projetosData: Array<Projeto> = [];
    public showModalProjetos: boolean = false;
    public modalProjetos: any = {};
    public modalProjetosId: string = '';
    public modalProjetosNome: string = '';
    public modalProjetosDescricao: string = '';
    public modalProjetosParticipante: string = '';

    public funcionariosData: Array<Usuario> = [];
    public showModalFuncionarios: boolean = false;
    public modalFuncionarios: any = {};
    public modalFuncionariosId: string = '';
    public modalFuncionariosNome: string = '';
    public modalFuncionariosUser: string = '';
    public modalFuncionariosEmail: string = '';
    public modalFuncionariosSenha: string = '';

    /**
     * Grids
     */
    @ViewChild(MatSort, { static: false }) gridSort: MatSort;
    @ViewChild(MatPaginator, { static: false }) gridPaginator: MatPaginator;

    public gridData: MatTableDataSource<any> = new MatTableDataSource();
    public gridColumns: Array<any> = [];
    public gridColumnsToDisplay: Array<string> = [];

    constructor(
        private appService: AppService,
        private snackBar: MatSnackBar) {

    }

    /**
     * Função responsável por exibir e ocultar a modal de login
     */
    public toggleLogin() {
        this.showLogin = !this.showLogin;
    }

    /**
     * Função responsável por enviar a requisição de login
     */
    public async doLogin() {
        const loginData = await this.appService.login(this.formLoginEmail, this.formLoginSenha);

        if (loginData.auth !== null && loginData.auth !== undefined && typeof loginData.auth === 'string') {
            const data = new Date();
            const jwt = loginData.auth === undefined ? '' : loginData.auth.toString();

            this.userData = loginData.user;
            this.appService.setJWT(jwt);
            this.userLoginData = `${data.getHours()}:${data.getMinutes()}`

            this.userIsLogged = true;
            this.showLogin = false;

            this.snackBar.open(`Bem vindo(a) ao sistema, ${loginData.user.nome}`, 'Fechar');
            this.getDataToView();
        }
        else {
            const error: any = loginData;
            const message = error.error === undefined ? 'Usuário ou senha inválidos.' : error.error.message.toString();

            this.userIsLogged = false;
            this.snackBar.open(message, 'Fechar');
        }
    }

    /**
     * Função responsável por obter os dados da view atual
     */
    public async getDataToView() {
        this.componentIsLoading = true;

        if (this.componentInView === 'FUNCIONARIOS') {
            if (this.funcionariosData.length === 0) {
                this.funcionariosData = await this.appService.getFuncionarios();
            }

            this.gridData.data = this.funcionariosData;
            this.gridColumns = [
                { name: '_id', display: 'Identificador' },
                { name: 'nome', display: 'Nome' },
                { name: 'usuario', display: 'Usuário' },
                { name: 'email', display: 'Email' },
                { name: 'cargo', display: 'Cargo' }
            ];

            if (this.userData.cargo === 9) {
                this.gridColumns.push({ name: 'controls', display: 'Ações' });
            }

            this.gridColumnsToDisplay = this.gridColumns.map(col => col.name);
        }
        else {
            if (this.projetosData.length === 0) {
                this.projetosData = await this.appService.getProjetos();
            }

            this.gridData.data = this.projetosData;
            this.gridColumns = [
                { name: '_id', display: 'Identificador' },
                { name: 'nome', display: 'Nome' },
                { name: 'descricao', display: 'Descrição' },
                { name: 'participantes', display: 'Participantes' },
            ];

            if (this.userData.cargo === 9) {
                this.gridColumns.push({ name: 'controls', display: 'Ações' });
            }

            this.gridColumnsToDisplay = this.gridColumns.map(col => col.name);
        }

        this.componentIsLoading = false;

        this.gridData.sort = this.gridSort;
        this.gridData.paginator = this.gridPaginator;
    }

    /**
     * Função responsável por alterar o componente na visualização
     */
    public goToView(component: any) {
        this.componentInView = component;
        this.getDataToView();
    }

    /**
     * Função responsável por abrir a modal
     */
    public openModalAdd() {
        if (this.componentInView === 'PROJETOS') {
            this.modalProjetos = {
                title: 'Adicionar um projeto',
                role: 'add'
            };

            this.showModalProjetos = true;
        }
        else {
            this.modalFuncionarios = {
                title: 'Adicionar um funcionário',
                role: 'add'
            };

            this.showModalFuncionarios = true;
        }
    }

    /**
     * Função responsável por abrir a modal de edicao
     */
    public openModalEdit(id: string) {
        if (this.componentInView === 'PROJETOS') {
            this.modalProjetos = {
                title: 'Editar o projeto',
                role: 'edit'
            };

            const projeto = this.projetosData.filter(e => e._id === id)[0];

            this.modalProjetosId = id;
            this.modalProjetosNome = projeto.nome;
            this.modalProjetosDescricao = projeto.descricao;
            this.modalProjetosParticipante = projeto.participantes[0];

            this.showModalProjetos = true;
        }
        else {
            this.modalFuncionarios = {
                title: 'Editar dados do funcionário',
                role: 'edit'
            };

            const funcionario = this.funcionariosData.filter(e => e._id === id)[0];

            this.modalFuncionariosId = id;
            this.modalFuncionariosNome = funcionario.nome;
            this.modalFuncionariosUser = funcionario.usuario;
            this.modalFuncionariosEmail = funcionario.email;
            this.modalFuncionariosSenha = '';

            this.showModalFuncionarios = true;
        }
    }

    /**
     * Função responsável por ocultar a modal de projetos
     */
    public hideModalProjetos() {
        this.modalProjetosId = '';
        this.modalProjetosNome = '';
        this.modalProjetosDescricao = '';
        this.modalProjetosParticipante = '';

        this.showModalProjetos = false;
    }

    /**
     * Função responsável por ocultar a modal de funcionarios
     */
    public hideModalFuncionarios() {
        this.modalFuncionariosId = '';
        this.modalFuncionariosNome = '';
        this.modalFuncionariosUser = '';
        this.modalFuncionariosEmail = '';
        this.modalFuncionariosSenha = '';

        this.showModalFuncionarios = false;
    }

    /**
     * Ação da modal de projetos
     */
    public async actionModalProjetos(role: 'add' | 'edit') {
        let message: string;
        let data: any;

        if (role === 'add') {
            data = await this.appService.addProjeto(this.modalProjetosNome, this.modalProjetosDescricao, [this.modalProjetosParticipante]);
            
            if (data.hasOwnProperty('status')) {
                message = data.error.message;
            }
            else {
                message = data.message;
            }
        }
        else {
            data = await this.appService.editProjeto(this.modalProjetosId, this.modalProjetosNome, this.modalProjetosDescricao, [this.modalProjetosParticipante]);
            
            if (data.hasOwnProperty('status')) {
                message = data.error.message;
            }
            else {
                message = data.message;
            }
        }

        this.hideModalProjetos();
        this.snackBar.open(message, 'Fechar');
        this.projetosData = [];
        this.getDataToView();
    }

    /**
     * Ação da modal de funcionarios
     */
    public async actionModalFuncionarios(role: 'add' | 'edit') {
        let message: string;
        let data: any;

        if (role === 'add') {
            data = await this.appService.addFuncionario(this.modalFuncionariosNome, this.modalFuncionariosUser, this.modalFuncionariosEmail, this.modalFuncionariosSenha);
            
            if (data.hasOwnProperty('status')) {
                message = data.error.message;
            }
            else {
                message = data.message;
            }
        }
        else {
            data = await this.appService.editFuncionario(this.modalFuncionariosId, this.modalFuncionariosNome, this.modalFuncionariosUser, this.modalFuncionariosEmail, this.modalFuncionariosSenha);
            
            if (data.hasOwnProperty('status')) {
                message = data.error.message;
            }
            else {
                message = data.message;
            }
        }

        this.hideModalFuncionarios();
        this.snackBar.open(message, 'Fechar');
        this.funcionariosData = [];
        this.getDataToView();
    }

    /**
     * Botão de remoção do grid
     */
    public async gridControlRemoveClick(id: string) {
        let message;

        if (this.componentInView === 'PROJETOS') {
            const data: any = await this.appService.removeProjeto(id);

            if (data.hasOwnProperty('status')) {
                message = data.error.message;
            }
            else {
                message = data.message;
            }

            this.projetosData = [];
        }
        else {
            const data: any = await this.appService.removeFuncionario(id);

            if (data.hasOwnProperty('status')) {
                message = data.error.message;
            }
            else {
                message = data.message;
            }

            this.funcionariosData = [];
        }

        this.snackBar.open(message, 'Fechar');
        this.getDataToView();
    }
}
