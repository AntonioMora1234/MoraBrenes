from flask import Flask, render_template, flash, request,url_for,redirect # se importa el modulo Flask (para el servidor web)
import BaseDatos  # se crea modulo de la base datos
from Validaciones import*
from Tiempo import*

# se crea el objeto conexion 
obj_sql = BaseDatos.Conexion()

app = Flask(__name__) # se crea el objeto flask

# esta es la seguridad de ella
app.secret_key = 'mysecretkey'

# Rutas 

@app.route('/')
def Inicio():
    return render_template('index.html')

@app.route('/RegistrarPuesto')
def RegistrarPuesto():
    return render_template('RegistrarPuesto.html')

@app.route('/Planilla')
def CargarPerfil_RH():
    return render_template('GestiionPlanilla.html')

@app.route('/loginRH') # Gestion de Planilla
def Login_RH():
    return render_template('Login_RH.html')

@app.route('/LoginPuesto') # Registrar Puesto
def LoginRH_Puesto():
    return render_template('LoginRH_puesto.html')

@app.route('/NuevoUsuario')
def NuevoUsuario():
    return render_template('RegistrarUsuario.html') 

@app.route('/perfil') 
def PerfilUsuario(): #Perfil del usuario
    return render_template('perfil_usuario.html')
@app.route('/loginUsuario')
def LoginUsuario():
    return render_template('login_usuario.html')

@app.route('/GestionPlinilla2')
def gestionPlanilla_holder():
    return render_template('CargarFormulario.html')    

@app.route('/Contacto')
def Contactos():
    obj_sql.AbrirConexion()
    resultado = obj_sql.ListarContactos()
    return render_template('Contactos.html', contactos = resultado)
    
@app.route('/incapacidad')
def Incapacidad():
    return render_template('incapacidad.html')

@app.route('/Acerca_de')
def Acerca_de():
    return render_template('Acerca_de.html')


# Metodos

@app.route('/Departamento', methods=['POST']) # Registra el departamento
def getDepto():
    if request.method == 'POST':
        if request.form.get('Registrar_dep'):
            nombre_departamento = request.form['NombreDep']

            # se valida que no haya campos vacios

            if ValidarVacio(nombre_departamento) == True:
                flash('No puede ver campos vacios')
            else:    
                obj_sql.AbrirConexion()
                obj_sql.InsertarDepto(nombre_departamento)
                flash('Nuevo Departamento registrado con exito')
        return redirect(url_for('RegistrarPuesto'))


@app.route('/Puesto', methods=['POST']) # Registra el puesto
def getPuesto():
    if request.method == 'POST':
        if request.form.get('Confirmar'):
            nombre_puesto = request.form['Nombre']
            descripcion = request.form['text_descripcion']
            salario_min = request.form['SalarioMin']
            salario_max = request.form['SalarioMax']
            titulos = request.form['Titulo']
            id_depto = request.form['id_depto']
            
            # se valida que no haya letras en campos numericos

            if (ValidarIdentificacion(id_depto) == True or (ValidarIdentificacion(salario_max) == True)
                or ValidarIdentificacion(salario_min) == True):
                flash('Error al ingesar datos , no se perimten letras')
                return redirect(url_for('RegistrarPuesto'))

            # se valida que no haya campos vacios

            elif (ValidarVacio(nombre_puesto) == True or ValidarVacio(salario_min) == True or 
                 ValidarVacio(salario_max) == True or ValidarVacio(descripcion) == True or 
                 ValidarVacio(titulos) == True or ValidarVacio(id_depto) == True):
                 flash('No se permiten campos vacios')
                 return redirect(url_for('RegistrarPuesto'))    
            else:
                obj_sql.AbrirConexion()
                auxid = int(id_depto)
                if obj_sql.InsertarPuesto(nombre_puesto,descripcion,salario_min,salario_max,titulos,auxid) is False:
                    flash('El Departamento de este puesto no a sido registrado') 
                    return redirect(url_for('RegistrarPuesto'))
                else:
                    flash('Puesto Registrado con exito')
                    return redirect(url_for('RegistrarPuesto'))


@app.route('/LoginRH_Puesto', methods=['POST']) # Login para entrar y registrar puesto y departamento
def get_loginRh_puesto():
    if request.method == 'POST':
        if request.form.get('InciarSesion'):
            usuario = request.form['user_id']
            password = request.form['user_pass']
            id_permiso = request.form['id_permiso']
            
            # se valida que no haya campos vacios

            if ValidarVacio(usuario) is True or ValidarVacio(password) is True or ValidarVacio(id_permiso) is True:
                flash('No pueden quedar campos vacios')
                return redirect(url_for('LoginRH_Puesto'))

            # se valida que no haya letras en campos numericos
            
            elif ValidarIdentificacion(id_permiso) is True:
                flash('No se permiten letra en el campo del id ') 
                return redirect(url_for('Login_RH'))
            
            # se valida que el password tenga 8 caracteres
            
            elif ValidarContrasenna(password) is True:
                flash('El Password no puede tener menos de 8 caracteres')
                return redirect(url_for('LoginRH_Puesto'))
            else:
                obj_sql.AbrirConexion()
                aux_idPermiso = int(id_permiso)
                if obj_sql.CargarLogin_RH(usuario,password,aux_idPermiso) is False: 
                    flash('El usuario no existe o tiene permisos')
                    return redirect(url_for('LoginRH_Puesto'))
                else:
                    obj_sql.AbrirConexion()
                    obj_sql.CargarLogin_RH(usuario,password,aux_idPermiso)
                    return redirect(url_for('RegistrarPuesto'))

@app.route('/Login_RH', methods=['POST']) # Incio de sesion para gestionar la planilla
def get_loginRh():
    if request.method == 'POST':
        if request.form.get('InciarSesion'):
            id_usuario = request.form['user_id']
            password = request.form['user_pass']
            id_permiso = request.form['id_permiso']
            if ValidarVacio(id_usuario) is True or ValidarVacio(password) is True or ValidarVacio(id_permiso) is True:
                flash('No pueden quedar campos vacios')
                return redirect(url_for('Login_RH'))

             # se valida que no haya campos vacios
            
            elif ValidarIdentificacion(id_permiso) is True:
                flash('No se permiten letra en el campo del id ') 
                return redirect(url_for('Login_RH'))
            
            # se valida que el password tenga 8 caracteres
            
            elif ValidarContrasenna(password) is True:
                flash('El Password no puede tener menos de 8 caracteres')
                return redirect(url_for('Login_RH'))
            else:
                obj_sql.AbrirConexion()
                aux_idPermiso = int(id_permiso)
                
            # Valida que el permiso sea 1 

                
                obj_sql.AbrirConexion()
                if  obj_sql.ValidaPermiso(id_permiso) is False:
                    flash('El permiso no es valido')
                    return redirect(url_for('Login_RH'))
             
                # Valida que coensidan el usuario,password y permiso
                
                if obj_sql.CargarLogin_RH(id_usuario,password,aux_idPermiso) is False: 
                    flash('El usuario no existe o tiene permisos')
                    return redirect(url_for('Login_RH'))
                
                else:
                    obj_sql.AbrirConexion()
                    obj_sql.CargarLogin_RH(id_usuario,password,aux_idPermiso)
                    return redirect(url_for('CargarPerfil_RH'))

@app.route('/NuevoUsuario', methods=['POST']) # Registra un nuevo usuario
def getUsuario():
    if request.method == 'POST':
        if request.form.get('Registrarse'):
            id_usuario = request.form['Identificacion']
            nombre = request.form['Nombre']
            primer_apellido = request.form['PrimerApellido']
            segundo_apellido = request.form['SegundoApellido']
            nacionalidad = request.form['Nacionalidad']
            direccion = request.form['Direccion']
            telefono = request.form['Telefono']
            password = request.form['Password'] 
            if ((ValidarVacio(id_usuario)) or ValidarVacio(nombre) or ValidarVacio(primer_apellido) or ValidarVacio(segundo_apellido)
               or ValidarVacio(nacionalidad) or ValidarVacio(direccion) or ValidarVacio(telefono) or ValidarVacio(password)
               is True):
               flash('No pueden ver campos vacios')
               return redirect(url_for('NuevoUsuario'))

            elif ValidarIdentificacion(id_usuario) or ValidarIdentificacion(telefono) is True:
                    flash('No se permiten letras en el en telefono o identificacion')
                    return redirect(url_for('NuevoUsuario'))            
            elif ValidarContrasenna(password) is True:
                flash('La contaseña debe tener mas de 8 caracteres')
                return redirect(url_for('NuevoUsuario'))

            elif ValodarCantidadIdentificacion(id_usuario) is True:
                flash('La identificacion no es valida') 
                return redirect(url_for('NuevoUsuario'))
            else:
                obj_sql.AbrirConexion()
                obj_sql.InsertarDatosUusarioNuevo(id_usuario,nombre,primer_apellido,segundo_apellido,password,nacionalidad,
                direccion,telefono)
                obj_sql.AbrirConexion()
                resultado = obj_sql.CargarPerfilUsuario(id_usuario,password)
                return render_template('perfil_usuario.html', resultado = resultado[0])
        else:
            if request.form.get('InciarSesion'):
                return redirect(url_for('LoginUsuario'))


"""
Actualiza el telefono del usuario
"""

@app.route('/info_cel/<id_usuario>')
def editCel(id_usuario):
    obj_sql.AbrirConexion()
    resultado = obj_sql.Datos_Usuario(id_usuario)
    return render_template('EditarTelefono.html', resultado = resultado[0])


@app.route('/upadte_cel/<id_usuario>' , methods=['POST'])
def ActualizarTelefono(id_usuario):
    if request.method == 'POST':
        if request.form.get('Aceptar'):
            telefono = request.form['Telefono']
            if ValidarVacio(telefono) is True:
                obj_sql.AbrirConexion()
                resultado = obj_sql.Datos_Usuario(id_usuario)
                flash('No se permiten campos vacios')
                return render_template('EditarTelefono.html', resultado = resultado[0])
            if ValidarIdentificacion(telefono) is True:
                obj_sql.AbrirConexion()
                resultado = obj_sql.Datos_Usuario(id_usuario)
                flash('No se permiten letras en el telefono')
                return render_template('EditarTelefono.html', resultado = resultado[0])
            else:         
                obj_sql.AbrirConexion()
                obj_sql.Actualizar_Usuario(id_usuario,None,telefono)
                flash('Datos actualizados correctamente')
                obj_sql.AbrirConexion()
                resultado = obj_sql.Datos_Usuario(id_usuario)
                return render_template('EditarTelefono.html', resultado = resultado[0])
    
                        
"""
Actualiza la direccion del usuario
"""

@app.route('/info_direccion/<id_usuario>')
def editDireccion(id_usuario):
    obj_sql.AbrirConexion()
    resultado = obj_sql.Datos_Usuario(id_usuario)
    return render_template('EditarDireccion.html', resultado = resultado[0])   

  

@app.route('/upadte_direccion/<id_usuario>' , methods=['POST'])
def ActualizarDireccion(id_usuario):
    if request.method == 'POST':
        if request.form.get('Aceptar'):
            direccion = request.form['Direccion']
            if ValidarVacio(direccion) is True:
                obj_sql.AbrirConexion()
                resultado = obj_sql.Datos_Usuario(id_usuario)
                flash('No se permiten campos vacios')
                return render_template('EditarDireccion.html', resultado = resultado[0])   
            else:         
                obj_sql.AbrirConexion()
                obj_sql.Actualizar_Usuario(id_usuario,direccion,None)
                flash('Datos actualizados correctamente')
                obj_sql.AbrirConexion()
                resultado = obj_sql.Datos_Usuario(id_usuario)
                return render_template('EditarDireccion.html', resultado = resultado[0])  
               

@app.route('/loginUsuario', methods=['POST'])                
def getLogin_usuario(): # Inicio de sesion del usuario
    if request.method == 'POST':
        if request.form.get('InciarSesion'):
            identificacion = request.form['user_id']
            password = request.form['user_pass']
            if ValidarVacio(identificacion) or ValidarVacio(password) is True:
                flash('No se permiten campos vacios')
                return redirect(url_for('LoginUsuario'))
            elif ValidarContrasenna(password) is True:
                flash('La contraseña no puede ser menor de 8 caracteres')
                return redirect(url_for('LoginUsuario'))    
            obj_sql.AbrirConexion()
            if obj_sql.CargarPerfilUsuario(identificacion,password) is False:
                flash('Usuario o password incorrectos') 
                return redirect(url_for('LoginUsuario'))
            else:    
                # Se verica si este usuario tiene calculos registrados
                obj_sql.AbrirConexion()
                planilla = obj_sql.LeerPlanilla(identificacion)
                long = len(planilla)
                if long == 0:
                    """
                    Cuando se registra por primera vez no va tener caculos de la planilla
                    ne la tabla
                    """
                    obj_sql.AbrirConexion()
                    resultado = obj_sql.CargarPerfilUsuario(identificacion,password)
                    return render_template('perfil_usuario.html', resultado = resultado[0])  
                else:
                    """
                    Si entra aqui es que hay un calculo de planilla para este usuario
                    """
                    obj_sql.AbrirConexion()
                    resultado = obj_sql.CargarPerfilUsuario(identificacion,password)
                    obj_sql.AbrirConexion()
                    planilla = obj_sql.LeerPlanilla(identificacion)
                    return render_template('PerfilUsuarioDatosPlanilla.html',resultado = resultado[0], planilla = planilla[0])    


    """
    Este metodo busca por identificacion
    """

@app.route('/formUsuario', methods=['POST']) 
def BuscarUsuarioPlanilla(): 
    if request.method == 'POST':
        if request.form.get('Buscar'): # se comprueba el boton del formulario (Buscar)
            identificacion = request.form['user_id']    
            if ValidarIdentificacion(identificacion) is True:
                flash('No se permiten letras en este campo')
                return redirect(url_for('CargarPerfil_RH'))
            
            elif ValidarVacio(identificacion) is True:    
                flash('No se permiten espacios en blanco')
                return redirect(url_for('CargarPerfil_RH'))  
            else:
                obj_sql.AbrirConexion()
                if obj_sql.Validad_idUsuario(identificacion) is False:
                    flash('Usuario no encontrado')
                    return redirect(url_for('CargarPerfil_RH'))
                else:
                   # Aqui es donde se cargan los datos si son validos aparecen en los inputs y tablas
                    
                    obj_sql.AbrirConexion()
                    resultado = obj_sql.BuscarUsuario(identificacion)
                    
                    obj_sql.AbrirConexion()
                    planilla = obj_sql.LeerPlanilla(identificacion)

                    longuitud = len(planilla)
                    
                    if longuitud == 0:
                        return render_template('CargarFormulario.html', resultado = resultado[0])
                    else:
                        return render_template('CargarFormularioPlanilla.html', resultado = resultado[0], planilla = planilla[0]) 
        else:
            if request.form.get('Inicio'):
                return redirect(url_for('Inicio'))
        
     
    """
    Este metodo actualiza la informacion del usuario
    por medio del boton buscar 
    """                                                        

@app.route('/formInput',methods=['POST'])                  
def updateDatos():# Modifica los datos sensibles del usuario
    if request.method == 'POST':
        if request.form.get('Guardar'): # Captura el boton guardar

            """
            Se obtiene los valores del formulario
            """
            identificacion = request.form['user_id']
            fecha = request.form['fecha']
            asociacion = request.form.get('user_aso')
            estado = request.form.get('user_estado')
            salario = request.form['Salario']
            cuenta = request.form['Cuenta']
            id_permiso = request.form.get('id_permiso')
            id_puesto = request.form.get('id_puesto')

            """
            Se revisa si la tabla planilla tiene un valor mayor 0 , es que
            tine un salario calculado
            """
            obj_sql.AbrirConexion()
            planilla = obj_sql.LeerPlanilla(identificacion)
            longuitud = len(planilla)
            if longuitud == 0: # si es igual cero el salario no a sido calculado

                # Valiadaciones

                """
                Valida que los campos no esten vacios
                """
                if (ValidarVacio(identificacion) or ValidarVacio(fecha) or ValidarVacio(salario) or ValidarVacio(cuenta) 
                is True):
                    flash('No se permiten campos en blanco')
                    obj_sql.AbrirConexion()
                    resultado = obj_sql.BuscarUsuario(identificacion)
                    return render_template('CargarFormulario.html',resultado = resultado[0])

                """
                Valida que no se pongan letras en campos numericos
                """

                if(ValidarIdentificacion(identificacion) or ValidarIdentificacion(cuenta) or ValidarIdentificacion(salario)
                  or ValidarIdentificacion(fecha) is True):
                   flash('No se permiten letras en la indentificacion,fecha,salario ,cuenta')
                   obj_sql.AbrirConexion()
                   resultado = obj_sql.BuscarUsuario(identificacion)
                   obj_sql.AbrirConexion() 
                   return render_template('CargarFormulario.html',resultado = resultado[0])   
                else:
                    """
                    Se abre la conexion y se pregunta si el id del puesto existe
                    """

                    obj_sql.AbrirConexion()
                    aux_idPuesto = int(id_puesto)
                    aux_salario = float(salario)
                    if obj_sql.ValidarPuesto_id(aux_idPuesto) is True:
                        obj_sql.AbrirConexion()
                        resultado = obj_sql.BuscarUsuario(identificacion)
                        obj_sql.AbrirConexion()
                        planilla = obj_sql.LeerPlanilla(identificacion)
                        flash('El id del puesto no a sido registrado') 
                        return render_template('CargarFormulario.html',resultado = resultado[0])
                          # Valida que el salario este entre el rango registrado
                    
                    """
                    Se verifica que salario no sea mayor o menor del registrado en el 
                    puesto (si es true es que el sueldo es menor o mayor al registrado)
                    """

                    if obj_sql.ValidarPuesto_Salario(aux_idPuesto,aux_salario) is True:
                        obj_sql.AbrirConexion()
                        resultado = obj_sql.BuscarUsuario(identificacion)
                        obj_sql.AbrirConexion()
                        planilla = obj_sql.LeerPlanilla(identificacion)
                        flash('El salario no puede ser mayor o menor de lo registrado en el puesto') 
                        return render_template('CargarFormulario.html',resultado = resultado[0])    
                  
                        """
                        Si entra a este (else) es que las validaciones son correctas y se puede modificar 
                        los datos
                        """
                    else:
                        obj_sql.AbrirConexion()
                        obj_sql.ModifcarDatosUsuario_RH(fecha,cuenta,estado,id_permiso,id_puesto,asociacion,aux_salario,identificacion)
                        obj_sql.AbrirConexion()
                        resultado = obj_sql.BuscarUsuario(identificacion)
                        obj_sql.AbrirConexion()
                        flash('Datos actualizados correctamente')

                        """
                        Se retorna CargarFormulario cuando el usuario no tiene un salario registrado
                        """
                        return render_template('CargarFormulario.html',resultado = resultado[0])       
                
            
                """
                Si entra a este (else) es que en  la tabla planilla hay un valor (mayor a cero) 
                """
            else:

                """
                Se valida que no haya campos vacios
                """

                if (ValidarVacio(identificacion) or ValidarVacio(fecha) or ValidarVacio(salario) or ValidarVacio(cuenta) 
                is True):
                    obj_sql.AbrirConexion()
                    resultado = obj_sql.BuscarUsuario(identificacion)
                    flash('No se permiten campos en blanco')
                    return render_template('CargarFormularioPlanilla.html', planilla = planilla[0], resultado = resultado[0])  

                
                """
                Se valida que no se metan letras en los campos numericos 
                """

                if(ValidarIdentificacion(identificacion) or ValidarIdentificacion(cuenta) or ValidarIdentificacion(salario)
                  or ValidarIdentificacion(fecha) is True):
                  flash('No se permiten letras en la indentificacion,fecha,salario ,cuenta')
                  obj_sql.AbrirConexion()
                  resultado = obj_sql.BuscarUsuario(identificacion)
                  obj_sql.AbrirConexion()    
                  return render_template('CargarFormularioPlanilla.html', planilla = planilla[0], resultado = resultado[0])  

                else:
                    obj_sql.AbrirConexion()
                    aux_idPuesto = int(id_puesto)
                    aux_salario = float(salario)
                    
                    """
                    Valida que el puesto este registrado
                    """
                    if obj_sql.ValidarPuesto_id(aux_idPuesto) is True:
                        obj_sql.AbrirConexion()
                        resultado = obj_sql.BuscarUsuario(identificacion)
                        obj_sql.AbrirConexion()
                        planilla = obj_sql.LeerPlanilla(identificacion)
                        flash('El id del puesto no a sido registrado') 
                        return render_template('CargarFormularioPlanilla.html', planilla = planilla[0], resultado = resultado[0])  
                    
                     
                    """
                    Se verifica que salario no sea mayor o menor del registrado en el 
                    puesto (si es true es que el sueldo es menor o mayor al registrado)
                    """
                    
                    if obj_sql.ValidarPuesto_Salario(aux_idPuesto,aux_salario) is True:
                        obj_sql.AbrirConexion()
                        resultado = obj_sql.BuscarUsuario(identificacion)
                        obj_sql.AbrirConexion()
                        planilla = obj_sql.LeerPlanilla(identificacion)
                        flash('El salario no puede ser mayor o menor de lo registrado en el puesto') 
                        return render_template('CargarFormularioPlanilla.html', planilla = planilla[0], resultado = resultado[0])     
                    else:
                        """
                        Si entra aqui es que paso las validaciones y puede modificar los datod 
                        """

                        obj_sql.AbrirConexion()
                        obj_sql.ModifcarDatosUsuario_RH(fecha,cuenta,estado,id_permiso,id_puesto,asociacion,aux_salario,identificacion)
                        obj_sql.AbrirConexion()
                        resultado = obj_sql.BuscarUsuario(identificacion)
                        obj_sql.AbrirConexion()
                        planilla = obj_sql.LeerPlanilla(identificacion)
                        flash('Datos actualizados correctamente')
                        return render_template('CargarFormularioPlanilla.html', planilla = planilla[0], resultado = resultado[0]) 
                        
        elif request.form.get('Atras'):
            return redirect(url_for('CargarPerfil_RH'))
            
        elif request.form.get('Calcular'):
            try:
                identificacion = request.form['user_id']
              
                if ValidarDia() is True: 

                    """
                    Se abre la conexion y se verifica si hay algun caluculo de salario registrado
                    """

                    obj_sql.AbrirConexion()
                    planilla = obj_sql.LeerPlanilla(identificacion)
                    longuitud = len(planilla)
                    
                    """
                    Si es es cero es que no tiene calculos registrados
                    """
                    
                    if longuitud == 0:
                        obj_sql.AbrirConexion()
                        obj_sql.CalculoPlanilla(identificacion)

                        obj_sql.AbrirConexion()
                        resultado = obj_sql.BuscarUsuario(identificacion)

                        obj_sql.AbrirConexion()
                        planilla = obj_sql.LeerPlanilla(identificacion)

                        """
                        Calcula la planilla , el trigger se ejecuta , pero necesita que solo al 
                        darle el boton aprobar se guarde en la tabla historial
                        para corregir esto se elimina momentaneamente se elemina 
                        esto se guarda en una tabla temporal

                        """
                        
                        obj_sql.AbrirConexion()
                     
                        flash('Planilla ' + identificacion + ' ' + 'calculada con exito')

                        return render_template('CargarFormularioPlanilla.html', resultado = resultado[0], planilla = planilla[0])
                    
                        """
                        Se entra a este (else) valida que si ya esta calculado el salario no se pueda volver a registrar, 
                        almenos que se elimine ese calculo
                        """
                    else:
                        if longuitud > 0:
                            obj_sql.AbrirConexion()
                            resultado = obj_sql.BuscarUsuario(identificacion)
                            obj_sql.AbrirConexion()
                            planilla = obj_sql.LeerPlanilla(identificacion)
                            flash('La planilla del usuario ' + identificacion + ' ' +  'ya a sido calculada')
                            return render_template('CargarFormularioPlanilla.html', resultado = resultado[0],planilla = planilla[0])
                
                
                    """
                    Si entra a este (else) es que no es jueves (no se puede calcular el salario) 
                    """

                else:
                    obj_sql.AbrirConexion()
                    planilla = obj_sql.LeerPlanilla(identificacion)
                    longuitud = len(planilla)
                    if longuitud == 0:
                        obj_sql.AbrirConexion()
                        resultado = obj_sql.BuscarUsuario(identificacion)
                        flash('El calculo del salario solo se puede cada jueves')   
                        return render_template('CargarFormulario.html',resultado = resultado[0])      
                    else:
                        obj_sql.AbrirConexion()
                        planilla = obj_sql.LeerPlanilla(identificacion)
                        obj_sql.AbrirConexion()
                        resultado = obj_sql.BuscarUsuario(identificacion)
                        flash('El calculo del salario solo se puede cada jueves') 
                        return render_template('CargarFormularioPlanilla.html', planilla = planilla[0], resultado = resultado[0])

            except Exception as e:
                print(e)
                flash(' Error ' + str(e))    
        
        elif request.form.get('Eliminar'):
            try:

                """
                Se captura el valor(identificacion(id_usuario)) para saber cual registro borrar 
                """
                identificacion = request.form['user_id']
              
                """
                Se verifica si este usario esta registrado en tabla Planilla_tmp
                """           
                obj_sql.AbrirConexion()
                planilla = obj_sql.LeerPlanilla(identificacion)
                
                """
                Si longuitud es cero esque no tiene datos, osea no tiene datos calculados
                por lo tanto no pueden ser borrados
                """
                longuitud = len(planilla)

                if longuitud == 0:
                    flash('Error , la planilla no a sido calculada')
                    obj_sql.AbrirConexion()
                    resultado = obj_sql.BuscarUsuario(identificacion)
                    return render_template('CargarFormulario.html',resultado = resultado[0])
                else:
                    obj_sql.AbrirConexion()
                    obj_sql.ElimianrPlanillaTMP(identificacion)

                    obj_sql.AbrirConexion()
                    resultado = obj_sql.BuscarUsuario(identificacion)

                    flash('Calculo eliminado con exito') 

        
                    return render_template('CargarFormulario.html',resultado = resultado[0])
               
            except Exception as e:
                flash('A habido un error ' + str(e))

        elif request.form.get('Aprobar'):
            identificacion = request.form['user_id']
            
            
            """
            Se pregunta el dia de aprobar la planilla , solo se puede aprobar el dia del caiculo
            (jueves)

            """
            
            if ValidarDia() is True:
                   
                """
                se lee la tabla planilla_tmp 
                """

                obj_sql.AbrirConexion()
                planilla = obj_sql.LeerPlanilla(identificacion)
                    
                """
                    Si longuitud es cero esque no tiene datos, osea no tiene datos calculados
                    por lo tanto no pueden ser borrados
                """
                longuitud = len(planilla)
                if longuitud == 0:
                    flash('Error , la planilla no a sido calculada')
                    obj_sql.AbrirConexion()
                    resultado = obj_sql.BuscarUsuario(identificacion)
                    return render_template('CargarFormulario.html',resultado = resultado[0])
                else:
                    obj_sql.AbrirConexion()
                    obj_sql.Elimianar_auxhistorial(identificacion)

                    obj_sql.AbrirConexion()
                    resultado = obj_sql.BuscarUsuario(identificacion)

                    obj_sql.AbrirConexion()
                    planilla = obj_sql.LeerPlanilla(identificacion)

                    flash('Planilla aprobada con exito')

                    return render_template('CargarFormularioPlanilla.html', planilla = planilla[0], resultado = resultado[0])
            else:
                obj_sql.AbrirConexion()
                planilla = obj_sql.LeerPlanilla(identificacion)
                obj_sql.AbrirConexion()
                resultado = obj_sql.BuscarUsuario(identificacion)
                flash('El calculo del salario solo se puede cada jueves') 
                return render_template('CargarFormularioPlanilla.html', planilla = planilla[0], resultado = resultado[0])
                
        elif request.form.get('Historial'):

            identificacion = request.form['user_id']
            
            """
            Se verifica si el usuario ya tiene un historial registrado 
            si longuitud es cero quere decir que no tiene un historal 
            registrado , entonces se retorna una pagina html sin datos (historial_sinCalculo.html)
            si tiene datos, se lee leer la base de datos y se imprime en una pagina html
            (Historial.html)
            """
            obj_sql.AbrirConexion()
            planilla = obj_sql.Cargar_historial(identificacion)
            longuitud = len(planilla)
            if longuitud == 0:
                return render_template('historial_sinCalculo.html')
            else:
                return render_template('Historial.html', planilla = planilla)


@app.route('/RegistroIncapacidad', methods=['POST'])
def  getIncapacidad():
    if request.method == 'POST':
        if request.form.get('Aceptar'):
            fecha_incio = request.form['Fecha_inicio']
            fecha_final = request.form['Fecha_final']
            motivo = request.form['motivo']
            id_usuario = request.form['id_usuario']

            # se valida que no haya letras en campos numericos
            
            if ValidarIdentificacion(fecha_final) or ValidarIdentificacion(fecha_incio) is True:
                flash('No se permiten letras en los campos')
                return redirect(url_for('Incapacidad'))
            
             # se valida que no haya campos vacios
            
            if ValidarVacio(motivo) or ValidarVacio(fecha_final) or ValidarVacio(fecha_incio) or ValidarVacio(id_usuario) is True:
                flash('No se permiten campos vacios')
                return redirect(url_for('Incapacidad'))
            
            # Valida que el id_usuario exista
            
            obj_sql.AbrirConexion()
            if obj_sql.Validad_idUsuario(id_usuario)  is False:
                flash('La identificacion no existe')
                return redirect(url_for('Incapacidad'))
            else:
                obj_sql.AbrirConexion()
                obj_sql.RegistrarIncapacidad(fecha_incio,fecha_final,motivo,id_usuario)
                flash('Incapacidad Rgistrado con exito')
                return redirect(url_for('Incapacidad'))

app.run(debug=False)
