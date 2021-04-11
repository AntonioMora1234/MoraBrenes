import pyodbc # se  importa el conector de sql server
from datetime import datetime

class Conexion: # se crea la clase conexion
    conexion = ""
    def AbrirConexion(self):
        try:
            # se pasan los parametros servidor.base datos, usuario y contraseña 
            self.conexion = pyodbc.connect('DRIVER={ODBC DRIVER 17 FOR SQL SERVER};' 'SERVER=localhost;' 'DATABASE=DB_Planilla;'
            'UID=Gabriel Moya;' 'PWD=123456')
            print('Conexion establecida')
            return True
        except Exception as e:
            print(e)
            
            
    def ListarContactos(self):
        try:
            cursor = self.conexion.cursor()
            consulta = "SELECT *FROM CONTACTOS"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            return resultado # retorna los datos de la tabla
        except Exception as e:
            print(e)
            
        finally:
            self.conexion.close()    
      
    def InsertarDatosUusarioNuevo(self,identificacion,Nombre,PrimerApellido,SegundoApellido,Password,Nacionalidad,Direccion,Telefono):
        try:
            cursor = self.conexion.cursor()
            datos = (identificacion,Nombre,PrimerApellido,SegundoApellido,Password,Nacionalidad,Direccion,Telefono)
            cursor.execute("{CALL InsertarUsuario (?,?,?,?,?,?,?,?)}",datos)
            cursor.commit()
            cursor.close()
        except Exception as e:
            print(e)
            
        finally:
            self.conexion.close()

    def CargarPerfilUsuario(self,identificacion,password):
        try:
            cursor = self.conexion.cursor()
            consulta = "SELECT *FROM Usuario"
            cursor.execute(consulta)
            resul = cursor.fetchall()
            p = -1
            for i in range(len(resul)):
                if identificacion == resul[i][0] and password == resul[i][4]:
                    p = i
                    break
            if p< 0:
                return False
            else:
                datos = (identificacion,password)
                cursor.execute("{CALL Perfil_Usuario (?,?)}",datos)
                resultado = cursor.fetchall()
                cursor.close()
                return resultado
               
        except Exception as e:
            print(e)    

        finally:
            self.conexion.close()

    
    
    def ValidaPermiso(self,id_permiso):
        try:
            cursor = self.conexion.cursor()
            consulta = "SELECT *FROM Usuario"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            p = -1
            for i in range(len(resultado)):
                if resultado[i][13] == 1:
                    p = i

            if p < 0:
                return False        

        except Exception as e:
            print(e)        

    
    def CargarLogin_RH(self,identificacion,password,id_permiso):
        try:
            cursor = self.conexion.cursor()
            consulta = "SELECT *FROM Usuario"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            p = -1
            for i in range(len(resultado)):
                if identificacion == resultado[i][0] and password == resultado[i][4] and id_permiso == resultado[i][13]:
                    p = i
                    break

            if p < 0:
                return False
            else:
                datos = (identificacion,password,id_permiso)
                cursor.execute("{CALL CargarPerfil_RH (?,?,?)}",datos)
                resultado= cursor.fetchall()
                cursor.close()
                return resultado
        except Exception as e:
            print(e)
        finally:
            self.conexion.close()        
        
             
    def BuscarUsuario(self,identificacion):
        try:
            cursor = self.conexion.cursor()
            datos = (identificacion)
            cursor.execute("{CALL BuscarUsuarioPlanilla(?)}",datos)
            resultado = cursor.fetchall()
            return resultado
           
        except Exception as e:
            print(e)    
        finally:
            self.conexion.close()    
    
    
    def ValidarPuesto_id(self,id_puesto): # Valida el id del puesto exista
        try:
            cursor = self.conexion.cursor()
            consulta = "SELECT *FROM Puesto"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            p = -1
            for i in range(len(resultado)):
                if id_puesto == resultado[i][0]:
                    p = i
                    break
            
            if p < 0: # El id no existe 
                return True
            else:
                return False # el id existe
              

        except Exception as e:
            print(e)    
    
    def ValidarPuesto_Salario(self,id_puesto,salario):# valida el salario del puesto
        try:
            cursor = self.conexion.cursor()
            consulta = "SELECT *FROM Puesto"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            for i in range(len(resultado)):
                if id_puesto == resultado[i][0]:
                    menor = int(resultado[i][3])
                    mayor = int(resultado[i][4])
            
            if salario < menor or salario > mayor:
                return True
            else:
                return False    
            cursor.close()    
        
        except Exception as e:
            print(e)    
    
    
    def Validad_idUsuario(self,id_usuario): # Valida que el id del usuario exista
        try:
            cursor = self.conexion.cursor()
            consulta = "SELECT *FROM Usuario"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            p = -1
            for i in range(len(resultado)):
                if id_usuario == resultado[i][0]:
                    p = i

            if p < 0:
                return False

            cursor.close()

        except Exception as e:
            print(e)         

    def ModifcarDatosUsuario_RH(self,fecha,cuenta,estado,id_permiso,id_puesto,asociacion,salario,identificacion):
        try:
            cursor = self.conexion.cursor() 
            datos = (fecha,cuenta,estado,id_permiso,id_puesto,asociacion,salario,identificacion)
            cursor.execute("{CALL ModificarUsuario_RH (?,?,?,?,?,?,?,?)}",datos) 
            cursor.commit()
            cursor.close()  
        except Exception as e:
            print(e)    
        finally:
            self.conexion.close()    

    def InsertarDepto(self,nombre):
        try:
            cursor = self.conexion.cursor()
            datos = (nombre)
            cursor.execute("{CALL InsertarDepto (?)}",datos)
            cursor.commit()
            cursor.close()
        except Exception as e:
            print(e)      
        finally:
            self.conexion.close()

    def InsertarPuesto(self,nombre,descripcion,salario_min,salario_max,titulos,id_depto):
        try:
            cursor = self.conexion.cursor()
            consulta = "SELECT *FROM Departamento"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            p = -1
            for i in range(len(resultado)):
                if id_depto == resultado[i][0]:
                    p = i
                    break

            if p<0:
                return False             
            else:
                datos = (nombre,descripcion,salario_min,salario_max,titulos,id_depto)
                cursor.execute("{CALL InsertarPuesto (?,?,?,?,?,?)}",datos)
                cursor.commit()
                cursor.close()
             
        except Exception as e:
            print(e)
        finally:
            self.conexion.close()          

    def RegistrarIncapacidad(self,fecha_inicio,fecha_final,motivo,id_usuario):

        try:
            cursor = self.conexion.cursor()
            datos = (fecha_inicio,fecha_final,motivo,id_usuario)
            cursor.execute("{CALL RegistrarIncapacidad (?,?,?,?)}",datos)
            cursor.commit()
            cursor.close()
        except Exception as e:
            print(e)    
        finally:
            self.conexion.close()    

    def CalculoPlanilla(self, identificacion):
        try:
            cursor = self.conexion.cursor()
            datos = (identificacion)
            cursor.execute("{CALL CalculoPlanilla (?)}",datos)
            cursor.commit()
            cursor.close()
            
        except Exception as e:
            print(e)     
        finally:
            self.conexion.close()
         
    def LeerPlanilla(self, id_usuario):
        try:
            cursor = self.conexion.cursor()
            datos = (id_usuario)
            consulta = "SELECT *FROM Planilla_tmp WHERE id_usuario = ?"
            cursor.execute(consulta,datos)
            resultado = cursor.fetchall()
            return resultado
        except Exception as e:
            print(e)
        finally:
            self.conexion.close()   
    
    def ValidarCaluculo_id(self, id_usuario):
        try:
            cursor = self.conexion.cursor()
            consulta = "SELECT *FROM Usuario"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            cursor.close()
            for i in range(len(resultado)):
                if id_usuario == resultado[i][0]:
                    return True
        except Exception as e:
            print(e)        
        finally:
            self.conexion.close()    

    def ElimianrPlanillaTMP(self,id_usuario):
        try:
            cursor = self.conexion.cursor()
            datos = (id_usuario)
            cursor.execute("{CALL EliminarPlanilla (?)}",datos)
            cursor.commit()
            cursor.close()

        except Exception as e:
            print(e)
        finally:
            self.conexion.close()        
    
    def Elimianar_auxhistorial(self,id_usuario):

        try:
            cursor = self.conexion.cursor()
            datos = (id_usuario)
            cursor.execute("{CALL EliminarPlanilla_aux (?)}",datos)
            cursor.commit()
            cursor.close()

        except Exception as e:
            print(e)
        finally:
            self.conexion.close()        
    
  
    def Cargar_historial(self, id_usuario):
        try:
            cursor = self.conexion.cursor()
            datos = (id_usuario)
            cursor.execute("{CALL CargarHistorial (?)}",datos)
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except Exception as e:
            print(e)        
        finally:
            self.conexion.close()            
    
    def Datos_Usuario(self, id_usuario):
        try:
            cursor = self.conexion.cursor()
            datos = (id_usuario)
            cursor.execute("{CALL Datos_Usuario(?)}",datos)
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except Exception as e:
            print(e)        
        finally:
            self.conexion.close()      
    def Actualizar_Usuario(self,id_usuario,direccion,telefono):
        try:
            cursor = self.conexion.cursor()
            datos = (id_usuario,direccion,telefono)
            cursor.execute("{CALL ActualizarDatos_usuario(?,?,?)}",datos)
            cursor.commit()
            cursor.close()
            
        except Exception as e:
            print(e)        
        finally:
            self.conexion.close()            
                
  

"""
obj  = Conexion()
obj.AbrirConexion()

x = obj.Datos_Usuario('305110782')
print(x)
"""




