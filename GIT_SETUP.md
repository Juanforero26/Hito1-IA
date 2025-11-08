# 🚀 Guía: Subir Código a Git

## ✅ Estado Actual

- ✅ Repositorio Git inicializado
- ✅ Commit inicial realizado
- ✅ Archivos agregados (43 archivos)
- ⏳ Pendiente: Conectar con repositorio remoto

---

## 📋 Próximos Pasos

### Opción 1: Si el Repositorio Remoto Ya Existe

Si ya tienes un repositorio en GitHub/GitLab/etc llamado "Hito1-IA", conecta con él:

```bash
# Agregar el repositorio remoto
git remote add origin URL_DEL_REPOSITORIO

# Verificar que se agregó correctamente
git remote -v

# Cambiar a la rama main (si es necesario)
git branch -M main

# Hacer push del código
git push -u origin main
```

**Ejemplo con GitHub:**
```bash
git remote add origin https://github.com/TU_USUARIO/Hito1-IA.git
git branch -M main
git push -u origin main
```

**Ejemplo con GitLab:**
```bash
git remote add origin https://gitlab.com/TU_USUARIO/Hito1-IA.git
git branch -M main
git push -u origin main
```

### Opción 2: Crear un Nuevo Repositorio en GitHub

1. **Ve a GitHub** y crea un nuevo repositorio:
   - Nombre: `Hito1-IA`
   - Descripción: "Sistema de pedidos institucionales de panadería"
   - Visibilidad: Público o Privado (tu elección)
   - **NO inicialices** con README, .gitignore o licencia

2. **Copia la URL** del repositorio (ej: `https://github.com/TU_USUARIO/Hito1-IA.git`)

3. **Conecta con el repositorio:**
```bash
git remote add origin https://github.com/TU_USUARIO/Hito1-IA.git
git branch -M main
git push -u origin main
```

---

## 🔧 Comandos Completos

### Si tu repositorio está en GitHub:

```bash
# 1. Agregar el remoto
git remote add origin https://github.com/TU_USUARIO/Hito1-IA.git

# 2. Cambiar a main (si GitHub usa main en lugar de master)
git branch -M main

# 3. Verificar el remoto
git remote -v

# 4. Hacer push
git push -u origin main
```

### Si tu repositorio está en GitLab:

```bash
# 1. Agregar el remoto
git remote add origin https://gitlab.com/TU_USUARIO/Hito1-IA.git

# 2. Cambiar a main
git branch -M main

# 3. Verificar el remoto
git remote -v

# 4. Hacer push
git push -u origin main
```

---

## 🐛 Solución de Problemas

### Error: "remote origin already exists"

Si ya existe un remoto, puedes:
1. **Ver el remoto actual:**
   ```bash
   git remote -v
   ```

2. **Eliminar el remoto y agregarlo de nuevo:**
   ```bash
   git remote remove origin
   git remote add origin URL_DEL_REPOSITORIO
   ```

3. **O cambiar la URL del remoto:**
   ```bash
   git remote set-url origin URL_DEL_REPOSITORIO
   ```

### Error: "failed to push some refs"

Si hay cambios en el remoto que no tienes localmente:

```bash
# Opción 1: Hacer pull primero y luego push
git pull origin main --allow-unrelated-histories
git push -u origin main

# Opción 2: Forzar el push (solo si estás seguro)
git push -u origin main --force
```

### Error: "authentication failed"

Necesitas autenticarte:

1. **Para HTTPS:** Usa un token de acceso personal
2. **Para SSH:** Configura tus llaves SSH

**Para GitHub:**
- Ve a Settings → Developer settings → Personal access tokens
- Crea un token con permisos de repositorio
- Usa el token como contraseña cuando hagas push

---

## ✅ Verificar que Funcionó

Después de hacer push, verifica:

1. **Ve a tu repositorio** en GitHub/GitLab
2. **Verifica que todos los archivos** estén presentes
3. **Verifica que el README.md** se muestre correctamente
4. **Verifica que no se hayan subido archivos sensibles** (`.env`, `.db`, `node_modules`)

---

## 📝 Archivos que NO se Subieron (Correcto)

Estos archivos están en `.gitignore` y NO se subieron:
- ✅ `.env` (variables de entorno sensibles)
- ✅ `*.db` (base de datos)
- ✅ `node_modules/` (dependencias)
- ✅ `.DS_Store` (archivos del sistema)

---

## 🔄 Para Futuros Cambios

Después de hacer cambios:

```bash
# 1. Ver qué archivos cambiaron
git status

# 2. Agregar los cambios
git add .

# 3. Hacer commit
git commit -m "Descripción de los cambios"

# 4. Hacer push
git push
```

---

## 📚 Buenas Prácticas

1. **Haz commits frecuentes** con mensajes descriptivos
2. **No subas archivos sensibles** (`.env`, tokens, etc.)
3. **Usa branches** para nuevas funcionalidades
4. **Mantén el README actualizado**
5. **Usa `.gitignore`** para excluir archivos innecesarios

---

## 🎯 Resumen

**Estado Actual:**
- ✅ Repositorio inicializado
- ✅ Commit inicial realizado
- ⏳ Pendiente: Conectar con remoto y hacer push

**Próximo Paso:**
```bash
git remote add origin URL_DEL_REPOSITORIO
git branch -M main
git push -u origin main
```

---

## 💡 Ayuda

Si necesitas ayuda:
1. Verifica la URL del repositorio
2. Verifica tus credenciales de GitHub/GitLab
3. Revisa los mensajes de error
4. Consulta la documentación de Git

