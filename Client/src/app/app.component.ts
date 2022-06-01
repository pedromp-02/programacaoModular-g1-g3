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
    public userData: Login;

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
    public funcionariosData: Array<Usuario> = [];
    public projetosData: Array<Projeto> = [];

    @ViewChild(MatSort, { static: false }) gridSort: MatSort;
    @ViewChild(MatPaginator, { static: false }) gridPaginator: MatPaginator;

    public gridData: MatTableDataSource<any> = new MatTableDataSource();
    public gridColumns: Array<any> = [];
    public gridColumnsToDisplay: Array<string> = [];

    constructor(
        private appService: AppService,
        private snackBar: MatSnackBar) {

        this.userData = new Login();
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

            this.userData = loginData;
            this.userLoginData = `${data.getHours()}:${data.getMinutes()}`

            this.userIsLogged = true;
            this.showLogin = false;

            this.snackBar.open(`Bem vindo(a) ao sistema, ${loginData.nome}`, 'Fechar');
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
}
