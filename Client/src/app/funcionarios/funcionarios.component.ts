import { Component, Input, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
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
    public data: Array<Usuario> = [];
    public componentIsLoading: boolean = true;

    public gridData: MatTableDataSource<any> = new MatTableDataSource();
    public gridColumns: Array<any> = [];
    public gridColumnsToDisplay: Array<string> = [];

    /**
     * Modal
     */
    public showModal: boolean = false;
    public modal: any = {};
    public modalDadosUsuario!: Usuario;
    public modalConfirmacaoSenha!: string;
    public modalHidePassword = true;
    public modalHidePasswordConfirmacao = true;

    /**
     * Modal detalhes
     */
    public showModalDetalhes: boolean = false;
    public modalDetalhesUserData!: Usuario;

    constructor(
        private appService: AppService,
        private snackBar: MatSnackBar) { }

    ngOnInit() {
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
     * Função responsável por filtrar o grid
     */
    public applyFilter(event: Event) {
        const filterValue = (event.target as HTMLInputElement).value;
        this.gridData.filter = filterValue.trim().toLowerCase();
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

            this.modalDadosUsuario = new Usuario();
            this.modalDadosUsuario.fillBlank();
            this.modalConfirmacaoSenha = '';
            this.showModal = true;
        }
        else {
            this.modal = {
                title: 'Editar dados do funcionário',
                role: 'edit'
            };

            const funcionario = this.data.filter(e => e._id === id)[0];
            this.modalDadosUsuario = Object.assign({}, funcionario);
            this.modalDadosUsuario.senha = '';
            this.modalConfirmacaoSenha = '';
            this.showModal = true;
        }
    }

    /**
     * Função responsável por ocultar a modal
     */
    public hideModal() {
        this.modalDadosUsuario = new Usuario();
        this.modalHidePassword = true;
        this.modalHidePasswordConfirmacao = true;
        this.modalConfirmacaoSenha = '';

        this.showModal = false;
    }

    /**
     * Função responsável por ocultar a modal de detalhes do funcionario
     */
    public hideModalDetalhes() {
        this.showModalDetalhes = false;
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

        if (!this.validaNome('funcionário', this.modalDadosUsuario.nome))
            return;
        
        if (!this.validaEmail())
            return;

        if (!this.validaCPF('digitado', this.modalDadosUsuario.cpf))
            return;

        if (!this.validaSalario())
            return;

        if (!this.validaData('nascimento', this.modalDadosUsuario.dataNascimento))
            return;

        if (!this.validaData('admissão', this.modalDadosUsuario.dataAdmissao))
            return;

        if (!this.validaSenha())
            return;

        for (let i = 0; i < this.modalDadosUsuario.dependentes.length; i++) {
            const dependente = this.modalDadosUsuario.dependentes[i];

            if (!this.validaNome(`dependente ${i + 1}`, dependente.nome))
                return;

            if (!this.validaCPF(`do dependente ${i + 1}`, dependente.cpf))
                return;
        }

        if (role === 'add') {
            data = await this.appService.addFuncionario(this.modalDadosUsuario);

            if (data.hasOwnProperty('status')) {
                message = data.error.message;
            }
            else {
                message = data.message;
            }
        }
        else {
            data = await this.appService.editFuncionario(this.modalDadosUsuario);

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

    public showDetailsFuncionario(funcionario: Usuario) {
        this.modalDetalhesUserData = funcionario;
        this.showModalDetalhes = true;
    }

    public addDependente(funcionario: Usuario) {
        funcionario.dependentes.push({
            cpf: '000.000.000-00',
            nome: '',
            parentesco: ''
        })
    }

    public removeDependente(funcionario: Usuario, index: number) {
        funcionario.dependentes = funcionario.dependentes.filter((e, i) => i !== index);
    }

    /**
     * Funções de validação dos dados
     */
    private validaNome(text: string, nome: string) {
        if (nome.search(" ") !== -1) {
            if (!(/^[a-zA-Zà-ùÀ-Ú ]+$/.test(nome))) {
                this.snackBar.open(`O nome do ${text} não está em um formato válido.`, 'Fechar');
                return false;
            }

            return true;
        }

        this.snackBar.open(`Digite o nome completo do ${text}`, 'Fechar');
        return false;
    }

    private validaEmail() {
        if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(this.modalDadosUsuario.email)) {
            return true;
        }

        this.snackBar.open('O email digitado não é válido.', 'Fechar');
        return false;
    }

    private validaCPF(text: string, cpf: string) {
        if (/^[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}$/.test(cpf)) {
            return true;
        }

        this.snackBar.open(`O CPF ${text} não está em um formato válido.`, 'Fechar');
        return false;
    }

    private validaSalario() {
        const salario = this.modalDadosUsuario.salario.toString();

        if (/^[0-9]*$/.test(salario) || /^[0-9]*.[0-9]{2}$/.test(salario) || /^[0-9]*,[0-9]{2}$/.test(salario)) {
            return true;
        }

        this.snackBar.open('O salário digitado não está em um formato válido.', 'Fechar');
        return false;
    }

    private validaData(text: string, campo: string) {
        if(!/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(campo)) {
            this.snackBar.open(`A data de ${text} não está em um formato válido.`, 'Fechar');
            return false;
        }

        var parts = campo.split("/");
        var day = parseInt(parts[0], 10);
        var month = parseInt(parts[1], 10);
        var year = parseInt(parts[2], 10);

        if(year < 1000 || year > 3000 || month == 0 || month > 12) {
            this.snackBar.open(`A data de ${text} não é válida.`, 'Fechar');
            return false;
        }

        var monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];

        if(year % 400 == 0 || (year % 100 != 0 && year % 4 == 0))
            monthLength[1] = 29;

        const currentDate = new Date();
        const campoDate = new Date(year, month - 1, day, 0, 0, 0, 0);

        if (day > 0 && day <= monthLength[month - 1] && campoDate.getTime() < currentDate.getTime()) {
            return true;
        }

        this.snackBar.open(`A data de ${text} não é válida.`, 'Fechar');
        return false;
    }

    private validaSenha() {
        if (this.modalDadosUsuario.senha.length === 0) {
            this.snackBar.open('A senha não pode ser vazia', 'Fechar');
            return false;
        }

        if (this.modalDadosUsuario.senha === this.modalConfirmacaoSenha) {
            return true;
        }

        this.snackBar.open('As senhas não são iguais', 'Fechar');
        return false;
    }
}
