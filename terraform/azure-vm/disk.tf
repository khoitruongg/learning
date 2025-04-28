# Data Disk
resource "azurerm_managed_disk" "data_disk" {
  name                 = "mydatadisk1"
  location             = azurerm_resource_group.rg.location
  resource_group_name  = azurerm_resource_group.rg.name
  storage_account_type = "Standard_LRS"
  create_option        = "Empty"
  disk_size_gb         = var.disk_size_gb
}

# Attach Data Disk to existing VM
resource "azurerm_virtual_machine_data_disk_attachment" "disk_attach" {
  managed_disk_id    = azurerm_managed_disk.data_disk.id
  virtual_machine_id = azurerm_linux_virtual_machine.vm.id

  lun                = 0
  caching            = "ReadOnly"
}

output "data_disk_id" {
  value = azurerm_managed_disk.data_disk.id
}
