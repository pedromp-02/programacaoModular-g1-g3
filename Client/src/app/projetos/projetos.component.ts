import { Component, Input, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatTableDataSource } from '@angular/material/table';
import { AppService } from '../app.service';
import { Participante, Projeto } from '../models/projetos.model';
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
    public funcionariosData: Array<Usuario> = [];
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
    public modalProjetoData!: Projeto;

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
            this.funcionariosData = await this.appService.getFuncionarios();
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
            this.modalProjetoData = new Projeto();
            this.modalProjetoData.fillBlank();
        }
        else {
            this.modal = {
                title: 'Editar o projeto',
                role: 'edit'
            };

            const projeto = this.data.filter(e => e._id === id)[0];
            this.modalProjetoData = projeto;
            this.showModal = true;
        }
    }

    /**
     * Função responsável por ocultar a modal
     */
    public hideModal() {
        this.modalProjetoData = new Projeto();
        this.modalProjetoData.fillBlank();
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

        if (!this.validaData('início', this.modalProjetoData.dataInicio))
            return;

        if (!this.validaData('término', this.modalProjetoData.dataFim))
            return;

        if (!this.comparaDatas())
            return;

        for (let i = 0; i < this.modalProjetoData.participantes.length; i++) {
            const participante = this.modalProjetoData.participantes[i];
    
            if (!this.validaHorario(participante.cargaHorariaSemanal.toString(), i))
                return;
        }

        if (role === 'add') {
            //data = await this.appService.addProjeto(this.modalProjetoData);

            if (data.hasOwnProperty('status')) {
                message = data.error.message;
            }
            else {
                message = data.message;
            }
        }
        else {
            //data = await this.appService.editProjeto(this.modalProjetoData);

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

    public getParticipantesProjeto(participantes: Array<Participante>) {
        let str = '';

        for (let i = 0; i < participantes.length; i++) {
            str += participantes[i].nome.split(" ")[0];

            if (i !== (participantes.length - 1)) {
                if (i === (participantes.length - 2)) {
                    str += ' e ';
                }
                else {
                    str += ', ';
                }
            }
        }

        return str;
    }

    public addParticipante(projeto: Projeto) {
        projeto.participantes.push({
            matricula: '',
            cargaHorariaSemanal: 0,
            nome: '',
            email: ''
        })
    }

    public removeParticipante(projeto: Projeto, index: number) {
        projeto.participantes = projeto.participantes.filter((e, i) => i !== index);
    }

    /**
     * Valida dados
     */
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

        if (day > 0 && day <= monthLength[month - 1]) {
            return true;
        }

        this.snackBar.open(`A data de ${text} não é válida.`, 'Fechar');
        return false;
    }

    private comparaDatas() {
        const partsInicio = this.modalProjetoData.dataInicio.split("/");
        const dayInicio = parseInt(partsInicio[0], 10);
        const monthInicio = parseInt(partsInicio[1], 10) - 1;
        const yearInicio = parseInt(partsInicio[2], 10);
        
        const partsFim = this.modalProjetoData.dataFim.split("/");
        const dayFim = parseInt(partsFim[0], 10);
        const monthFim = parseInt(partsFim[1], 10) - 1;
        const yearFim = parseInt(partsFim[2], 10);
        
        const dataInicio = new Date(yearInicio, monthInicio, dayInicio);
        const dataFim = new Date(yearFim, monthFim, dayFim);

        if (dataFim.getTime() > dataInicio.getTime()) {
            return true;
        }

        this.snackBar.open(`A data de término deve ser maior que a data de início`, 'Fechar');
        return false;
    }

    private validaHorario(campo: string, i: number) {
        if (/^[0-9]*$/.test(campo)) {
            return true;
        }

        this.snackBar.open(`A carga horária do participante ${i + 1} não está em um formato válido.`, 'Fechar');
        return false;
    }
}
